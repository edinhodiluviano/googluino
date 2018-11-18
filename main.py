#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 22:59:57 2018

@author: edinho
"""

#%%

import time

import re
import sys
import urllib
import asyncio
import logging
import datetime

import requests
import pandas as pd
from bs4 import BeautifulSoup

import metadata

#%%

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s]: %(message)s', 
    level=logging.INFO
)

#%%

class BaseExtractor(object):
    
    def __init__(self, name: str, data: dict):
        self.data = data
        self.name = name
    
    def query(self, query_string):
        self.get(query_string)
        self.extract_items()
        return self.items
    
    def url(self, query_string):
        query_string = urllib.parse.quote(query_string)
        return self.data['url'].replace('<query>', query_string)
    
    def get(self, query_string):
        if self.data['http']['method'] == 'get':
            self.http_response = requests.get(self.url(query_string))
        elif self.data['http']['method'] == 'post':
            self.data['http']['data']
            self.http_response = requests.post(self.url(query_string),
                                               data=self.data['http']['data'],
                                               headers=self.data['http']['headers'])
        else:
            raise NotImplementedError(f"Site {self.name} HTTP method {self.data['http']['method']} not implemented")
        if self.http_response.status_code != 200:
            raise requests.ConnectionError(f"Site {self.name}; expected status code 200, but got {self.http_response.status_code}")
    
    def extract_items(self):
        self.soup = BeautifulSoup(self.http_response.text, 'lxml')
        self.items = self.soup.find_all(self.is_item)
        self.items = [self.item_details(item) for item in self.items]
    
    def is_item(self, tag):
        for rule in self.data['item']['rules']:
            try:
                if eval(rule) != self.data['item']['rules'][rule]:
                    return None
            except AttributeError:
                return None
        return tag
    
    def item_details(self, item_soup):
        item = {}
        item['soup'] = item_soup
        for detail in self.data['item']['details']:
            try:
                item[detail] = eval(self.data['item']['details'][detail])
            except:
                print(f'\nvars:', 'site:"{self.name}"', 'detail:"{detail}"',
                       'url:{self.http_response.url}\n', sep='\n\t')
                raise
        if 'price' in item:
            self.convert_price_to_float(item)
        if 'name' in item:
            item['name'] = self.normalize_string(item['name'])
        return item

    def convert_price_to_float(self, item):
        item['price'] = item['price'].replace('.', '').replace('R$', '')
        item['price'] = item['price'].replace(',','.').replace(' ', '')
        if item['price'] == 'Preçosobconsulta':
            del item['price']
        else:
            item['price'] = float(item['price'])
    
    def normalize_string(self, string):
        string = re.sub('[ \n\r]+', ' ', string)
        return string

#%%

async def extract_site(site_name, site_data, query_string):
    """
    A coroutine to extract data from a site
    """
    logging.info(f'Extracting site {site_name}')
    extractor = BaseExtractor(site_name, site_data)
    items = extractor.query(query_string)
    
    return items

#%%

async def main(query_string):
#	"""
#	Creates a group of coroutines and waits for them to finish
#	"""
    
    coroutines = []
    for n, (site_name, site_data) in enumerate(metadata.SITES.items()):
        coroutines.append(extract_site(site_name, site_data, query_string))
    
    completed, pending = await asyncio.wait(coroutines)
    
    items = []
    for partial_items in completed:
        items = items + partial_items.result()
        
    return items
        
 
#%%

if __name__ == '__main__':
    if len(sys.argv) > 1:
        query_string = ' '.join(sys.argv[1:])
        
        now = datetime.datetime.now()
        
        event_loop = asyncio.get_event_loop()
        try:
            items = event_loop.run_until_complete(main(query_string))
        finally:
            event_loop.close()
        
        now2 = datetime.datetime.now()
        logging.info(f'total time: {now2-now}')
        
        n = len(metadata.SITES.items())
        df = pd.DataFrame(items)
        df.drop(['soup'], axis=1, inplace=True)
        filename = f"results"
        filename += f"_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"
        filename += f"_{query_string.replace(' ','_')}"
        filename += ".csv"
        df.to_csv(filename, index_label='n')
        logging.info(f'Searched {n} sites. Found {len(items)} results. Results saved to {filename}\n')

#%%
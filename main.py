#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 22:59:57 2018

@author: edinho
"""

#%%

import re
import sys
import json
import urllib
import datetime

import requests
import pandas as pd
from bs4 import BeautifulSoup

import metadata

#%%

class Lojas(object):
    
    def __init__(self, url='https://garoa.net.br/wiki/Lojas', filename='lojas.json'):
        self.filename = filename
        self.url = url
        self.load()
        return
    
    def load(self):
        try:
            with open(self.filename, 'r') as f:
                self.list = json.load(f)   
        except FileNotFoundError:
            self.list = []
        return 
    
    def save(self):
        with open(self.filename, 'w+') as f:
            return json.dump(self.list, f)
        
    def update(self, save=True):        
        #get garoa site
        resp = requests.get(self.url)
        if resp.status_code != 200:
            raise requests.ConnectionError(f'Expected status code 200, but got {resp.status_code}')
            return
        #parse it
        soup = BeautifulSoup(resp.text)
        start_tag = soup.find("span", id="Componentes_para_Arduino").parent
        end_tag = start_tag.find_next('h2')
        self.list = []
        while start_tag.next_sibling != end_tag:
            if start_tag.next_sibling != '\n':
                item = {}
                if start_tag.next_sibling.find('dt').find('a'):
                    item['name'] = start_tag.next_sibling.find('dt').find('a').text
                    item['url'] = start_tag.next_sibling.find('dt').find('a')['href']
                else:
                    item['name'] = start_tag.next_sibling.find('dt').text
                    item['url'] = None
                item['desc'] = start_tag.next_sibling.find_all('dd')[-1].text
                self.list.append(item)
            start_tag = start_tag.next_sibling        
        #persist the results (or not)
        if save == True:
            self.save()        
        return
    
    
    
    
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

if __name__ == '__main__':
    if len(sys.argv) > 1:
        query_string = ' '.join(sys.argv[1:])
        items = []
        print()
        for n, (site_name, site_data) in enumerate(metadata.SITES.items()):
            extractor = BaseExtractor(site_name, site_data)
            temp_items = extractor.query(query_string)
            items = items + temp_items
            print(f'n: {n}', f'query: "{query_string}"', f'site: {site_name}', f'items: {len(temp_items)}', sep='\t')
        df = pd.DataFrame(items)
        df.drop(['soup'], axis=1, inplace=True)
        filename = f"results"
        filename += f"_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"
        filename += f"_{query_string.replace(' ','_')}"
        filename += ".csv"
        df.to_csv(filename, index_label='n')
        print(f'Searched {n} sites. Found {len(items)} results. Results saved to {filename}\n')

#%%


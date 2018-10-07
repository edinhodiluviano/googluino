#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 19:26:19 2018

@author: edinho
"""


SITES = {
    'newport':{
        'domain':'newportcom.com.br',
        'url':'http://newportcom.com.br/catalogsearch/result/index/?limit=12&q=<query>',
        'http':{
            'method':'get',
        },
        'item':{
            'rules':{
                "tag.name":'li',
                "tag.has_attr('class')":True,
                "tag.parent.name":'ul',
                "tag.parent.has_attr('class')":True,
                "tag.parent.parent.name":'div',
                "tag.parent.parent.has_attr('class')":True,
                "tag.parent.parent['class'][0]":'category-products',
            },
            'details':{
                'name':"item['soup'].find('h2', {'class':'product-name'}).find('a').text",
                'url':"item['soup'].find('h2', {'class':'product-name'}).find('a')['href']",
                'price':"item['soup'].find('div', {'class':'price-box'}).find('span', {'class':'price'}).text",
            },
        },
    },
    'mscnbrasil':{
        'domain':'mscnbrasil.com.br',
        'url':'http://www.mscnbrasil.com.br/buscas.php?search_query=<query>',
        'http':{
            'method':'get',
        },
        'item':{
            'rules':{
                "tag.name":'li',
                "tag.has_attr('class')":True,
                "tag.parent.name":'ul',
                "tag.parent.has_attr('class')":True,
                "tag.parent['class']":['ProductList', 'Clear'],
            },
            'details':{
                'name':"item['soup'].find('div', {'class':'ProductDetails'}).find('a').text",
                'url':"item['soup'].find('div', {'class':'ProductDetails'}).find('a')['href']",
                'price':"item['soup'].find('div', {'class':'ProductPriceRating'}).find('em').text",
            },
        },
    },
    'hperobotica':{
        'domain':'hperobotica.com.br',
        'url':'http://www.hperobotica.com.br/search.html',
        'http':{
            'method':'post',
            'headers':{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'},
            'data':{'searchQuery':'<query>'},
        },
        'item':{
            'rules':{
                "tag.name":"div",
                "tag.has_attr('class')":True,
                "tag['class'][0]":'product-item-container',
            },
            'details':{
                'name':"item['soup'].find('div',{'class':'iluria-layout-search-product-title'}).find('a').text",
                'url':"item['soup'].find('div',{'class':'iluria-layout-search-product-title'}).find('a')['href']",
                'price':"item['soup'].find('span',{'class':'product-price-text'}).text",
            },
        },
    },
    'multcomercial':{
        'domain':'multcomercial.com.br',
        'url':'https://loja.multcomercial.com.br/catalogsearch/result/?q=<query>',
        'http':{
            'method':'get',
        },
        'item':{
            'rules':{
                "tag.name":'li',
                "tag.has_attr('class')":True,
                "tag['class']":['item','last'],
            },
            'details':{
                'name':"item['soup'].find('h2',{'class':'product-name'}).find('a').text",
                'url':"item['soup'].find('h2',{'class':'product-name'}).find('a')['href']",
                'price':"item['soup'].find('span',{'class':'price'}).text",
            },
        },
    },
    'filipeflop':{
        'domain':'filipeflop.com',
        'url':'https://www.filipeflop.com/?s=<query>&post_type=product',
        'http':{
            'method':'get',
        },
        'item':{
            'rules':{
                "tag.name":'li',
                "tag.has_attr('class')":True,
                "tag.parent.name":'ul',
                "tag.parent.has_attr('class')":True,
                "tag.parent['class']":['products','columns-4'],
            },
            'details':{
                'name':"item['soup'].find('h2',{'class':'woocommerce-loop-product__title'}).text",
                'url':"item['soup'].find('a',{'class':'woocommerce-LoopProduct-link woocommerce-loop-product__link'})['href']",
                'price':"item['soup'].find('span',{'class':['woocommerce-Price-amount','amount']}).text", 
            },
        },
    },
    'baudaeletronica':{
        'domain':'baudaeletronica.com.br',
        'url':'https://www.baudaeletronica.com.br/catalogsearch/result/?q=<query>',
        'http':{
            'method':'get',
        },
        'item':{
            'rules':{
                "tag.name":'li',
                "tag.has_attr('class')":True,
                "tag['class']":['item'],
            },
            'details':{
                'name':"item['soup'].find('h2',{'class':'product-name'}).find('a').text",
                'url':"item['soup'].find('h2',{'class':'product-name'}).find('a')['href']",
                'price':"item['soup'].find('span',{'class':['price']}).text", 
            },
        },
    },
}



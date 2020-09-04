
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
#import re
#import time
from datetime import datetime
#import matplotlib.dates as mdates
#import matplotlib.ticker as ticker
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

#print("Input Amazon product list url")
#website = input()
website=("https://www.amazon.com.au/gp/bestsellers/toys/ref=zg_bs_toys_home_all?pf_rd_p=546999f6-cd7b-4e25-ba30-e1af343370e3&pf_rd_s=center-1&pf_rd_t=2101&pf_rd_i=home&pf_rd_m=ANEGB3WVEVKZB&pf_rd_r=4MYWJPAQJ0T8Q1VCWM0V&pf_rd_r=4MYWJPAQJ0T8Q1VCWM0V&pf_rd_p=546999f6-cd7b-4e25-ba30-e1af343370e3")

no_pages = 1

def get_data(pageNo):  
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    r = requests.get(website+str(pageNo)+'?ie=UTF8&pg='+str(pageNo), headers=headers)#, proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content)
    #print(soup)

    prodListMaster = []
    for d in soup.findAll('div', attrs={'class':'a-section a-spacing-none aok-relative'}):
        #print(d)
        product = d.find('span', attrs={'class':'zg-text-center-align'})
        n = product.find_all('img', alt=True)
        #print(n[0]['alt'])
        producerAuthor = d.find('a', attrs={'class':'a-size-small a-link-child'})
        amazonRating = d.find('span', attrs={'class':'a-icon-alt'})
        customerRated = d.find('a', attrs={'class':'a-size-small a-link-normal'})
        listPrice = d.find('span', attrs={'class':'p13n-sc-price'})
        position = d.find('span', attrs={'class':'zg-badge-text'})

        prodList=[]

        if position is not None:
            #print(price.text)
            prodList.append(position.text)
        else:
            prodList.append('0') 

        if product is not None:
            #print(n[0]['alt'])
            prodList.append(n[0]['alt'])
        else:
            prodList.append("unknown-product")

        if producerAuthor is not None:
            #print(author.text)
            prodList.append(producerAuthor.text)
        elif producerAuthor is None:
            producerAuthor = d.find('span', attrs={'class':'a-size-small a-color-base'})
            if producerAuthor is not None:
                prodList.append(producerAuthor.text)
            else:    
                prodList.append('0')

        if amazonRating is not None:
            #print(rating.text)
            prodList.append(amazonRating.text)
        else:
            prodList.append('No rating')

        if customerRated is not None:
            #print(price.text)
            prodList.append(customerRated.text)
        else:
            prodList.append('0')     

        if listPrice is not None:
            #print(price.text)
            prodList.append(listPrice.text)
        else:
            prodList.append('0')
        prodListMaster.append(prodList)    
    return prodListMaster


results = []
for i in range(1, no_pages+1):
    results.append(get_data(i))
flatten = lambda l: [item for sublist in l for item in sublist]
database = pd.DataFrame(flatten(results),columns=['Position','Product','Producer / Author','Amazon Rating','Customers Rated','Listed Price'])
database.to_csv('amazon_products.csv', index=False, encoding='utf-8')

database = pd.read_csv("amazon_products.csv")
print(database)


#print('Enter Amazon Product ID')
#productId = input()

#def get_data(pageNo):  
#    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

#    r = requests.get('https://www.amazon.com.au/dp/'+productId, headers=headers)#, proxies=proxies)
#    content = r.content
#    soup = BeautifulSoup(content)
    #print(soup)

#    prodIdListMaster = []
#    for d in soup.findAll('div', attrs={'class':'centerColAlign centerColAlign-bbcxoverride'}):
        #print(d)

#        productPrice = d.find('a', attrs={'class':'a-size-medium a-color-price priceBlockBuyingPriceString'})

#        prodIdList=[]

#        prodIdList.append(productId)
#        prodIdList.append(productPrice)
#        prodIdListMaster.append(prodIdList) 
#    return prodIdListMaster

#results2 = []
#for i in range(1, no_pages+1):
#    results2.append(get_data(i))
#flatten2 = lambda l: [item for sublist in l for item in sublist]
#database2 = pd.DataFrame(flatten2(results2),columns=['Product','Listed Price'])
#database2.to_csv('amazon_product.csv', index=False, encoding='utf-8')

#database2 = pd.read_csv("amazon_product.csv")
#print(database2)
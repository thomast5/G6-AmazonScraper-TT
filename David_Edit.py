import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import os


#print("Input Amazon product list url")  #removed import for speed of testing
#website = input()
website = "https://www.amazon.com.au/gp/bestsellers/toys/ref=zg_bs_toys_home_all?pf_rd_p=546999f6-cd7b-4e25-ba30-e1af343370e3&pf_rd_s=center-1&pf_rd_t=2101&pf_rd_i=home&pf_rd_m=ANEGB3WVEVKZB&pf_rd_r=4MYWJPAQJ0T8Q1VCWM0V&pf_rd_r=4MYWJPAQJ0T8Q1VCWM0V&pf_rd_p=546999f6-cd7b-4e25-ba30-e1af343370e3"
no_pages = 1


def get_data(pageNo):  
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    r = requests.get(website+str(pageNo)+'?ie=UTF8&pg='+str(pageNo), headers=headers)#, proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content,features="html5lib") #lxml game me errors, html5lib worked
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
        #DB: added this section to append date time to last column   
        if datetime is not None:  
            #print(date.text)
            prodList.append(datetime.now())
               
        else:
            prodList.append('0')
            
        prodListMaster.append(prodList)    
    return prodListMaster


results = []
for i in range(1, no_pages+1):
    results.append(get_data(i))
flatten = lambda l: [item for sublist in l for item in sublist]
database = pd.DataFrame(flatten(results),columns=['Position','Product','Producer / Author','Amazon Rating','Customers Rated','Listed Price','Datetime'])

#David Edit
# if file does not exist create a csv 
if not os.path.isfile('amazon_products1.csv'):
   database.to_csv('amazon_products1.csv', index=False, encoding='utf-8')
else: # else it exists create another csv
   database.to_csv('amazon_products2.csv', index=False, encoding='utf-8')

#compare option, only works after running twice (two csv's need to exist)
with open('amazon_products1.csv', 'r') as t1, open('amazon_products2.csv', 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()
#output file if anything different (always will be because of timestamp)
with open('changes_found.csv', 'w') as outFile:
    for line in filetwo:
        if line not in fileone:
            outFile.write(line)

print ("Output as of : ",datetime.now())
print('\n')
print(database)

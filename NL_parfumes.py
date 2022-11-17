# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 08:28:28 2022

@author: vaneb
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import os
import time

product_nr = 0
product_list = []

driver = webdriver.Chrome(r'C:\Python\envs\chromedriver')

url = 'https://www.parfumvergelijker.nl/geuren/'
#158

driver.get(url)


while True:
    
    next_page_btn = driver.find_element(By.XPATH,".//*[@class='next page-numbers']")
    
    #loop through pages
    if not next_page_btn:
        
        break
    
    else:
        #search for product section
        products = driver.find_elements(By.XPATH,".//*[@class='product-wrapper']")
        
        links = []
        
        for i in range(len(products)):
            
            links.append(products[i].get_attribute('href'))
        
        #loop through products
        for idx, prod_link in enumerate(links):
          
            driver.get(prod_link)
            print(f"Off to scraping product {idx+1}")
            
            prod_info = driver.find_elements(By.ID,'product-single')
            
            for info in prod_info:
                
                image_url_src = info.find_element(By.TAG_NAME,'img').get_attribute('src')
                brand = info.find_element(By.CLASS_NAME,'product-details-brand').text
                model = info.find_element(By.CLASS_NAME,'product-details-model').text
                
                product_name = info.find_element(By.TAG_NAME,'img').get_attribute('alt')
                product_link_href = driver.current_url
                type1 = ' '.join(info.find_element(By.CLASS_NAME,'labels').text.split(' ')[:-1])
                gender = model.split(' ')[-1]

        
            sizes = driver.find_elements(By.CLASS_NAME,'size-group')
            
            for size in sizes:
                
                ml = size.find_element(By.CLASS_NAME,'tab').text.split(' ')[0]
                By.TAG_NAME
                #search for multiple items within size group
                items = size.find_elements(By.XPATH,".//*[@class='row shop']")
                
                for item in items:
                    
                    prod_id = product_link_href.split('/')[-2]
                    price_new = item.find_element(By.XPATH,".//*[@class='price-container']/span").text
                    try:
                        price_old = item.find_element(By.XPATH,".//*[@class='price-container']/del").text
                    except:
                        price_old = price_new

                    shop_img_url = item.find_element(By.TAG_NAME,'img').get_attribute('src')
                    shop_name = item.find_element(By.XPATH,'.//*[contains(@class, "info")]').text.split('-')[0].strip()

        
                    product_info = {'product_link_href':product_link_href,
                                    'brand':brand,
                                    'Type':type1,
                                    'gender':gender,
                                    'image_url_src':image_url_src,
                                    'product_id':prod_id,
                                    'shop_img_url':shop_img_url,
                                    'shop_name':shop_name,
                                    'Price_old':price_old,
                                    'Price_new':price_new,
                                    'ml':ml
                                    }
                
       
        
                    product_list.append(product_info)
                    product_nr += 1
           
            
            #### click back and choose next product
            driver.back()

        element = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,".//*[@class='next page-numbers']")))
        element.click()
        print("next page......")
        
df = pd.DataFrame(product_list)

df.to_csv('Product_list.csv',index=False)

print(f"Done for {product_nr} products.")
    
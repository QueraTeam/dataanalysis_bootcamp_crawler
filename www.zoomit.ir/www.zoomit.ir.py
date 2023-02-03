import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd


options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

driver.get('https://www.zoomit.ir/product/list/mobile/1/')

names_of_products = []
prices_of_products = []
new_price = []
final_price = []
my_dict = {}
driver.get('https://www.zoomit.ir/product/list/mobile/1/')

#getting names of product in the first page
product_names = driver.find_elements(By.CSS_SELECTOR, '.productTitle')
for i in product_names:
    names_of_products.append(i.text)

#getting prices of the product in the first page
product_price = driver.find_elements(By.CSS_SELECTOR, '.productSummery__prices--highlited span')
for i in product_price:
    prices_of_products.append(i.text)

#cleaning the prices string
for j in range(len(product_price)):
    if j%2 ==0:
        new_price.append(prices_of_products[j])

for j in range(len(new_price)):
    if j%2 !=0 :
         final_price.append(new_price[j])




#saving to a csv file via pandas datafram
df = pd.DataFrame(list(zip(names_of_products,final_price)), columns=['Names','Prices'])
df.to_csv('data.csv')








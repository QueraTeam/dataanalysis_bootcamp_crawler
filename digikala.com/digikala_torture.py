import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import json
import pandas as pd
import numpy as np
import re
import math

mapping = {
    '۰': '0',
    '۱': '1',
    '۲': '2',
    '۳': '3',
    '۴': '4',
    '۵': '5',
    '۶': '6',
    '۷': '7',
    '۸': '8',
    '۹': '9',
    '.': '.',
    }
def multiple_replace(text , mapping=mapping):
    """
    Internal function for replace all mapping keys for a input string
    :param mapping: replacing mapping keys
    :param text: user input string
    :return: New string with converted mapping keys to values
    """
    pattern = "|".join(map(re.escape, mapping.keys()))
    return re.sub(pattern, lambda m: mapping[m.group()], str(text))

opt = Options()
opt.headless = True
driver = webdriver.Chrome(options=opt) #options=opt
driver.implicitly_wait(7)
driver.maximize_window()
driver.get("https://www.digikala.com/search/?has_selling_stock=1&q=flash%2064gb")
driver.implicitly_wait(10)
def xpath_builder(get_option,get_value,get_state):
    return f'//{get_option}[@{get_value}="{get_state}"]'

option,value,state = "h3","class","ellipsis-2 text-body2-strong color-700"
datas_name = driver.find_elements(By.XPATH,xpath_builder(option,value,state))
for data in datas_name:
    print(data.text)

option,value,state = "div","class","d-flex ai-center jc-end gap-1 color-700 color-400 text-h5 grow-1"
datas_price = driver.find_elements(By.XPATH,xpath_builder(option,value,state))

for ind , data in enumerate(datas_price):
    print(data.text)

    
j={   "number":[z for z in range(1,len(datas_name)+1)],
      "name":[x.text.replace(",","") for x in datas_name],
      "price":[y.text.replace(",","") for y in datas_price]}
    
converted_nums = []
for key in j["price"]:
    string = multiple_replace(key)
    converted_nums.append(string)
j["price"] = converted_nums

df = pd.DataFrame.from_dict(j)
df.to_csv(os.path.dirname(__file__)+"\\prices.csv")

dataf = pd.read_csv(os.path.dirname(__file__)+"\\prices.csv",index_col="number")
dataf.drop("Unnamed: 0",axis=1,inplace=True)
print(dataf.describe())
print(dataf["price"].mean())

mean_price = dataf["price"].mean()

f = []

for price in dataf["price"]:
    diff = 1000000
    f.append(int(price)-mean_price)
    if abs(int(price)-mean_price) < diff:
        diff = int(price)-mean_price

for i,d in enumerate(f) :
    if diff == d:
        index_closest = i - 1
    else:
        pass

print(f"most close price of product to mean calculated in this program is index : {index_closest} and name is : {datas_name[index_closest].text} so value is : {datas_price[index_closest].text}")   

driver.quit()
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
import logging
from logging.handlers import RotatingFileHandler

dirname = os.path.dirname(__file__)

logging.basicConfig(filename=dirname+'\\report.txt',filemode="w",format='[TIME: %(asctime)s] [DigiKala@Torture] %(levelname)s: %(message)s', level=logging.INFO) #filename='Practices/log.log',
LOGGER = logging.getLogger("digikala@torture")


def syslogger(msg, sev = "info"):
    if "debug" in sev :
        LOGGER.debug(msg)        
    elif "info" in sev :
        LOGGER.info(msg)
    elif "warning" in sev :
        LOGGER.warning(msg)
    elif "error" in sev :
        LOGGER.error(msg)
    elif "critical" in sev :
        LOGGER.critical(msg)
    else:
        pass


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
syslogger("getting to https://www.digikala.com/search/?has_selling_stock=1&q=flash%2064gb")
driver.implicitly_wait(10)
syslogger("implicit wait set 10 sec!")

def xpath_builder(get_option,get_value,get_state):
    syslogger(f'xpath builder invoked! //{get_option}[@{get_value}="{get_state}"]')
    return f'//{get_option}[@{get_value}="{get_state}"]'
try:
    option,value,state = "h3","class","ellipsis-2 text-body2-strong color-700"
    datas_name = driver.find_elements(By.XPATH,xpath_builder(option,value,state))
except Exception as e :
    syslogger(sev="error",msg = e)

datas_name_text = []
for data in datas_name:
    datas_name_text.append(data.text.encode().decode('utf-8-sig'))
syslogger(f"{datas_name_text}")

try:
    option,value,state = "div","class","d-flex ai-center jc-end gap-1 color-700 color-400 text-h5 grow-1"
    datas_price = driver.find_elements(By.XPATH,xpath_builder(option,value,state))
except Exception as e :
    syslogger(sev="error",msg = e)
    
datas_price_text = []
for ind , data in enumerate(datas_price):
    datas_price_text.append(data.text.encode().decode('utf-8-sig'))
syslogger(f"{datas_price_text}")

try:    
    j={   "number":[z for z in range(1,len(datas_name)+1)],
          "name":[x.text for x in datas_name],
          "price":[y.text.replace(",","") for y in datas_price]}
except Exception as e :
    syslogger(sev="error",msg = e)
    
converted_nums = []
for key in datas_price:
    con = key.text.replace(',','')
    string = multiple_replace(con)
    converted_nums.append(string)
j["price"] = converted_nums
syslogger(f"gathering data to save as csv and parse it as dataFrame! data as dict is :{j}")

try:
    df = pd.DataFrame.from_dict(j)
    df.to_csv(os.path.dirname(__file__)+"\\prices.csv",mode="w")
except Exception as e :
    syslogger(sev="error",msg = e)
try:
    dataf = pd.read_csv(os.path.dirname(__file__)+"\\prices.csv",index_col="number")
    dataf.drop("Unnamed: 0",axis=1,inplace=True)
    syslogger(f"{dataf.describe()}")

    mean_price = dataf["price"].mean()
    syslogger(f"mean is {mean_price}")

    f = []
    diff = 1000000
    for price in dataf["price"]:
        f.append(int(price)-mean_price)
        if abs(int(price)-mean_price) < abs(diff):
            diff = int(price)-mean_price
    # for i,d in enumerate(f) :
    #     big_border = 1
            
    syslogger(f"closest value dif is : {diff}")
    for i,d in enumerate(f) :
        if diff == d:
            index_closest = i
        else:
            pass

except Exception as e :
    syslogger(sev="error",msg = e)
finally:
    syslogger(f"most close price of product to mean calculated in this program is index : {index_closest+1} and name is : {datas_name[index_closest].text.encode().decode('utf-8-sig')} so value is : {datas_price[index_closest].text.encode().decode('utf-8-sig')}") 
driver.quit()
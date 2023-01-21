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
import requests # برای استفاده از «ای پی آی» به این کتابخونه نیاز هست.

dirname = os.path.dirname(__file__)

logging.basicConfig(filename=dirname+'/report.txt',filemode="w",format='[TIME: %(asctime)s] [DigiKala@Torture] %(levelname)s: %(message)s', level=logging.INFO) #filename='Practices/log.log',
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

def api_way(): # این تابع از «ای پی آی» برای تولید اون فایل «سی اس وی» استفاده می‌کنه.
    df = pd.DataFrame(columns=["name"	,"price"	,"rrp_price"	,"order_limit"])
    n_page = 1
    while True:
        print(n_page)
        url = "https://api.digikala.com/v1/search/?has_selling_stock=1&q=flash%2064gb&page="+str(n_page)
        page = requests.get(url)
        mahsoolat = json.loads(page.text)["data"]["products"]
        if len(mahsoolat) == 0:
            break
        dict_ = {}
        dict_["name"] = [i["title_fa"] for i in mahsoolat]
        dict_["price"] = [i["default_variant"]["price"]["selling_price"] for i in mahsoolat]
        dict_["rrp_price"] = [i["default_variant"]["price"]["rrp_price"] for i in mahsoolat]
        dict_["order_limit"] = [i["default_variant"]["price"]["order_limit"] for i in mahsoolat]

        # dict to DataFrame
        df_ = pd.DataFrame(dict_)
        df = pd.merge(df , df_ , how='outer' )
        n_page+=1
    df.to_csv(os.path.dirname(__file__)+"/prices.csv",mode="w")

def selenium_way(Firefox_or_chrome):
    opt = Options()
    opt.headless = True
    if Firefox_or_chrome == "c": #‌اینجا اگر مخاطب کروم رو نداشت ولی فایرفاکس رو داشت ابزار بازم کار می‌کنه.
        driver = webdriver.Chrome(options=opt) #options=opt
    elif Firefox_or_chrome == "f":    
        driver = webdriver.Firefox()
    else:
        syslogger("invalid sign for selenium driver. (only use f or c)")
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
        df.to_csv(os.path.dirname(__file__)+"/prices.csv",mode="w") # آدرس دهیی قبلی که از \\ استفاده می‌کرد روی سیستم من که لینوکس بود خطا می‌داد تغییرات لازم رو بدین.
    except Exception as e :
        syslogger(sev="error",msg = e)
    driver.quit() # با تغییرات جدید نیازی به باز موندن درایور تا پایان برنامه نیست.
def gozaresh_dehi():
    try:
        dataf = pd.read_csv(os.path.dirname(__file__)+"/prices.csv") # آدرس دهیی قبلی که از \\ استفاده می‌کرد روی سیستم من که لینوکس بود خطا می‌داد تغییرات لازم رو بدین.
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
        syslogger(f'most close price of product to mean calculated in this program is index : {index_closest+1} and name is : {dataf["name"][index_closest]} so value is : {dataf["price"][index_closest]}') # اینجا یک تفاوتی وجود داره اگر از سلنیوم استفاده بشه به تومان قیمت اعلام می‌شه و اگر از «ای پی آی» استفاده بشه به ریال قیمت اعلام می‌شه.    
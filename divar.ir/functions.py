import json
import requests
import pandas as pd
import numpy
import time
from tokens import bale_token , bale_chat_id


def send_to_bale(matn):
    base_url = "https://tapi.bale.ai/bot"+bale_token+"/sendMessage"


    #id خودم رو توی بله پیدا کردم و اینجا قرار دادم
    parameters = {"chat_id":bale_chat_id , "text": matn}
    r = requests.get(base_url, params=parameters)

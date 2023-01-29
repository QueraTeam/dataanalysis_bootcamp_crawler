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



def api_divar_to_DataFrame(response):
    agahi_ha = json.loads(response.text)["web_widgets"]["post_list"]

    
    
    dict_ = {}
    dict_["لینک"] = []
    dict_["عنوان"] = []
    dict_["قیمت"] = []
    dict_["مکان"] = []

    for x in agahi_ha:
        dict_["لینک"].append(("https://divar.ir/v/"+x["data"]["action"]["payload"]["web_info"]["title"]+"/"+x["data"]["action"]["payload"]["token"]).replace(" ","_"))
        
        dict_["عنوان"].append(x["data"]["title"])
        
        dict_["قیمت"].append(x["data"]["middle_description_text"])
        dict_["مکان"].append(x["data"]["bottom_description_text"].split("در")[-1])
    df_ = pd.DataFrame(dict_).set_index("لینک")
    #print(dict_["عنوان"])
    return df_
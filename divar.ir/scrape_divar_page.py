# %%

import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import time
import os
from functions import send_to_bale
# %%

url = "https://api.divar.ir/v8/web-search/3/residential-sell"
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
"accept-language": "en-US,en;q=0.9,fa;q=0.8"}
data = {"json_schema":{"category":{"value":"residential-sell"},"cities":["3"]},"last-post-date":1774384963529066}
session = requests.Session()
response = session.post(url, headers=headers, json=data)



def api_divar_to_DataFrame(response):
    agahi_ha = json.loads(response.text)["web_widgets"]["post_list"]

    
    
    dict_ = {}
    dict_["لینک"] = []
    dict_["عنوان"] = []
    dict_["قیمت"] = []
    dict_["مکان"] = []

    for x in agahi_ha:
        dict_["لینک"].append("https://divar.ir/v/"+x["data"]["action"]["payload"]["web_info"]["title"]+"/"+x["data"]["action"]["payload"]["token"])
        
        dict_["عنوان"].append(x["data"]["title"])
        
        dict_["قیمت"].append(x["data"]["middle_description_text"])
        dict_["مکان"].append(x["data"]["bottom_description_text"].split("در")[-1])
    df_ = pd.DataFrame(dict_).set_index("لینک")
    #print(dict_["عنوان"])
    return df_
df_ = api_divar_to_DataFrame(response)
# %%

df_[0:1]
# %%
if "data.csv" not in os.listdir():
    df = pd.DataFrame(columns=["لینک" , "عنوان" , "قیمت" , "مکان"]).set_index("لینک")
else:
    df = pd.read_csv("data.csv").set_index("لینک")

# %%
df = pd.merge(df_ , df , how='outer' , on=["لینک" , "عنوان" , "قیمت" , "مکان"])
df.reset_index(inplace=True)
df.to_csv("data.csv" , index=False)


# %%

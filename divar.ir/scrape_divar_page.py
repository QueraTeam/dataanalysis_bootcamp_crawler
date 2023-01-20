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
url = "https://divar.ir/s/mashhad/buy-residential"

page = requests.get(url)

# %%
# اینجا کمک می‌کنه بفهمیم چه چیزایی استخراج شده
# این طور که به نظر می‌رسه توی دیوار این صفحه که ذخیره می‌شه با مرورگر که بازش می‌کنیم یک لحظه نمایش می‌ده ولی یک هو همون جوری آفلاین که هست خطای ۴۰۴ نمایش می‌ده.
f = open("what_scraped.html" , "w")
f.write(page.text)
f.close()

# %%
def divar_page_to_DataFrame(page):
    soup = BeautifulSoup(page.text , "html.parser")

    mored_ha = soup.find_all("div"  , class_ = "post-card-item-af972 kt-col-6-bee95 kt-col-xxl-4-e9d46")

    dict_ = {}
    dict_["لینک"] = []
    dict_["عنوان"] = []
    dict_["قیمت"] = []
    dict_["مکان"] = []

    for x in mored_ha:
        dict_["لینک"].append("https://divar.ir"+x.find("a" , href =True, class_ ="")["href"])
        
        dict_["عنوان"].append(x.find("h2",class_ = "kt-post-card__title").text)
        
        dict_["قیمت"].append(x.find("div",class_ = "kt-post-card__description").text)
        dict_["مکان"].append(x.find("span",class_ = "kt-post-card__bottom-description kt-text-truncate").text.split("در")[-1])
    df_ = pd.DataFrame(dict_).set_index("لینک")
    #print(dict_["عنوان"])
    return df_
df_ = divar_page_to_DataFrame(page)
# %%
if "data.csv" not in os.listdir():
    df = pd.DataFrame(columns=["لینک" , "عنوان" , "قیمت" , "مکان"]).set_index("لینک")
else:
    df = pd.read_csv("data.csv").set_index("لینک")

df = pd.merge(df , df_ , how='outer' )
df.to_csv("data.csv")


# %%
df
# %%
df_
# %%
df = pd.DataFrame(columns=["لینک" , "عنوان" , "قیمت" , "مکان"]).set_index("لینک")
df
# %%
df = pd.merge(df , df_ , how='outer' )
df
# %%

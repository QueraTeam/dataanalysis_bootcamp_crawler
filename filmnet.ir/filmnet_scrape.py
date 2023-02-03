#Libraries
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import pandas as pd
from collections import OrderedDict

# List to Append Information
title = []
rate = []
year = []
age_restriction = []
typee = []
origin = []
duration = []
imdb_rank = []
keshvar_sazandeh=[]

for i in range(10):
    url = "https://filmnet.ir/api-v2/video-contents?offset=" + str(24*i) + "&count=24&order=latest&query=&types=single_video&types=series&types=video_content_list"
    session = requests.Session() #prevent error about HTTPS Connect
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    page = session.get(url)
    j = json.loads(page.text)
    for k in range(24):
        #print(k)
        title.append(j['data'][k]['title'])
        rate.append(round(j['data'][k]['rate'],2))
        try:
            year.append(j['data'][k]['year'])
        except:
            year.append('---------')
        age_restriction.append(j['data'][k]['age_restriction'])
        typee.append(j['data'][k]['type'])
        origin.append(j['data'][k]['original_name'])
        try:
            duration.append(j['data'][k]['duration'])
        except KeyError:
            duration.append('---------')
        try:
            imdb_rank.append(j['data'][k]['imdb_rank_percent'])
        except KeyError:
            imdb_rank.append('Not Mentioned')
            
        categories=j['data'][k]['categories']
        territory_index = next((index for (index, d) in enumerate(categories) if d["type"] == "territory"), None)
        if territory_index == None:
            keshvar_sazandeh.append('Unknown')
        else:
            countries= " - ".join([ii['title'] for ii in categories[territory_index]['items']]).strip()
            keshvar_sazandeh.append(countries)
            

movies_info= OrderedDict()
movies_info['نام اثر'] = title
movies_info['رأی'] = rate
movies_info["رأی در IMDB"] = imdb_rank
movies_info['سال ساخت'] = year
movies_info['محدودیت سنی'] = age_restriction
movies_info['نوع'] = typee
movies_info['نام انگلیسی'] = origin
movies_info['زمان'] = duration
movies_info['کشور سازنده'] = keshvar_sazandeh
movies_info_df= pd.DataFrame(movies_info)





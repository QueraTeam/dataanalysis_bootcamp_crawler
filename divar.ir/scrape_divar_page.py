# %%
import json
import requests
import pandas as pd
import numpy
import time
from functions import send_to_bale
# %%
url = "https://divar.ir/s/mashhad/buy-residential"

page = requests.get(url)

# %%
f = open("what_scraped.html" , "w")
f.write(page.text)
f.close()

# %%
url = "https://api.divar.ir/v8/web-search/3/ROOT"
# %%
#                                                                                                      1674207963881798
parametr = {"json_schema":{"category":{"value":"ROOT"},"query":"خانه","cities":["3"]},"last-post-date":1674207963889798}
# %%
page = requests.post(url , data = parametr)

# %%
json.dumps(page.text)
# %%
page
# %%

# %%

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
url = "https://api.divar.ir/v8/web-search/3/residential-sell"
page = requests.get(url)

# %%
json.dumps(page.text)
# %%
page.text
# %%

# %%

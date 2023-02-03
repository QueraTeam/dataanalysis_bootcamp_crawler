import scrapy
import time
from selenium import webdriver 
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..items import Game


class SteamStoreSpider(scrapy.Spider):
    name = 'steamSpider'
    allowed_domains = ['store.steampowered.com']
    start_urls =      ['https://store.steampowered.com/search']

    driver = webdriver.Firefox()
    driver.get('https://store.steampowered.com/search')
    time.sleep(10)  # wait 10 seconds for website to fully load
    scroll_pause_time = 3 # 3 seconds delay to scroll the page
    screen_height = driver.execute_script("return window.screen.height;")   # getting the screen height of the page
    i = 1
    games = None
    while True:
        # scroll one screen height
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            games = BeautifulSoup(driver.page_source, "html.parser")
            break 
    
       
    print(games)
    def parse(self, games):
        for game in games.css("#search_resultsRows a"):
            title = game.css("span.title::text").get()
            url   = game.css("a::attr(href)").get()
            # url   = url.encode('ascii', errors='ignore')
            item = Game(title = title, url = url)
            yield item


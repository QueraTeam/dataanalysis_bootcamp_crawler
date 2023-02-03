import scrapy
import time
from selenium import webdriver 
from bs4 import BeautifulSoup
import json
from ..items import Game


class SteamStoreSpider(scrapy.Spider):
    name = 'steamSpider'
    allowed_domains = ['store.steampowered.com']
    start_urls =      ['https://store.steampowered.com/search/results/?query&start=0&count=50']

    
    def parse(self, response):
        for game in response.css("#search_resultsRows a"):
            title         = game.css("span.title::text").get()
            url           = game.css("a::attr(href)").get()
            date_released = game.css("div.search_released::text").get()
            price         = game.css("div.search_price::text").get()
            
            item = Game(title = title, url = url, date_released = date_released, price = price.strip())
            yield item
        
        
        splitted = response.url.split('start=')
        p_l = splitted[1].split('&')
        start_item = p_l[0]
        number_of_items = int(start_item) + 51
        if number_of_items < 2000:
            next_page_url = splitted[0] + 'start=' + str(number_of_items) + '&' + p_l[1] 
            yield scrapy.Request(next_page_url)


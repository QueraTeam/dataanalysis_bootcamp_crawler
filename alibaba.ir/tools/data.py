from .alibaba_crawler import *
from bs4 import BeautifulSoup

class TOUR(CrawlerTool):
    def __init__(self, browser: str, **tripdict: dict) -> None:
        super().__init__(browser)
        self._url +='/tour' 
        self.origin = tripdict['origin']
        self.destination = tripdict['destination']
        self.departure_date = tripdict['departure_date']
        self.return_date = tripdict['return_date']
        if 'rooms' in tripdict:
            self.rooms = tripdict['rooms']
        else:
            self.rooms = 1
        self._make_url()
   
    
    def _make_url(self,):

        self.driver.get(self._url)
        WebDriverWait(self.driver, 4).until(
                                            EC.presence_of_element_located((
                                                By.XPATH, '/html/body/div/div[1]/main/div/'\
                                                            'div[2]/div[2]/div[2]/div/div/div/div[1]')))

        search1 = self.driver.find_element(
            By.XPATH,
            '//*[contains(concat( " ", @class, " " ),' \
            'concat( " ", "mb-0", " " ))]//*[contains(concat('\
            ' " ", @class, " " ), concat( " ", "is-first", " " ))]//input')
        search1.send_keys()
        search1.send_keys(self.origin)
        try:
            WebDriverWait(self.driver, 1).until(
                    EC.element_located_to_be_selected(
                        (By.XPATH, "/html/body/div/div[1]/main/div/div[2]/div[1]"\
                        "/div[2]/div/form/div/div[1]/div/div[2]/"\
                        "div/ul/li[2]/a/span/span/span[1]")))
        except:
            pass
        html =  self.driver.page_source
        link_origin = BeautifulSoup(html, 'html.parser')
        ul = link_origin.find('ul', {'class':'a-menu pretty-scroll'})
        link_origin = ul.find('li')
        self.origin = link_origin['data-value']
        search = self.driver.find_element(
                                By.XPATH,
                                 '//*[contains(concat( " ", @class, " " ),'\
                                 ' concat( " ", "mb-0", " " ))]//*[contains(concat( " ", @class, " " ),'\
                                 ' concat( " ", "is-last", " " ))]//input')
        search.send_keys()
        search.send_keys(self.destination)
        try:
            WebDriverWait(self.driver, 1).until(
                EC.element_located_to_be_selected(
                    (By.XPATH,
                    '/html/body/div/div[1]/main/div/div[2]'\
                    '/div[1]/div[2]/div/form/div/div[1]/div/'\
                    'div[2]/div/ul/li[2]/a/span/span/span[1]')))
        except:
            pass
        html =  self.driver.page_source
        link_destination = BeautifulSoup(html, 'html.parser')
        ul = link_destination.find('ul', {'class':'a-menu pretty-scroll'})
        link_destination = ul.find('li')
        self.destination = link_destination['data-value']

        self._url = f'https://www.alibaba.ir/tour/{self.origin}/'\
        f'{self.destination}?from={self.departure_date}'\
        f'&to={self.return_date}&rooms={self.rooms}'
        print(self._url)
        self._open_page()

    def _open_page(self):
        self.driver.get(self._url)
        delay = 3
        while True:
            try:
                WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="app"]/div[1]/main/div/div/div/section/div[3]')))
                delay = 3
                break
            except TimeoutException:
                if delay == 5:
                    self.driver.refresh()
                    delay = 1
                delay += 1
                continue

        while True:
            try:
                WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="app"]/div[1]/main/div/div/div/section/div[3]')))
                break
            except TimeoutError:
                delay += 1
        while True:
            try:
                results = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/main/div/div/'\
                                                                'div/aside/div/div/div[1]/div/p/b')
                break                                        
            except:
                continue                                       
        if results.text == '0':
            raise Exception('Unfortunately, the tour was not found according to your search')                                             
                
                
        div = '/html/body/div/div[1]/main/div/div/div/section/div[3]/div'
        while True:
            try:
                WebDriverWait(self.driver, delay).until(EC.presence_of_element_located(
                (By.XPATH,
                '//*[@id="app"]/div[1]/main/div/div/div/section/div[3]')))
                break
            except TimeoutException:
                delay += 1 
                continue
        
        while True:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            if len(self.driver.find_elements(By.XPATH, div)) == int(results.text) + 1:
                info_result = self.driver.find_elements(By.XPATH, div)
                break
        loc_info = []
        for num,result in enumerate(info_result, 1):
            loc = f'/html/body/div/div[1]/main/div/div/div/section/div[3]/div[{num}]/div/div/div[1]/div/div[2]/div[2]/ul/li[1]'
            try:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                    (
                        By.XPATH, loc
                    )
                )).click()
            except:
                continue
            merge = False
            check = False
            count = 0
            texts = result.text.split('\n')
            for text in texts:
                if text == '+' or text == '-' or  text == 'بستن' or text == '_' :
                    continue
                if text == 'با احتساب حمل و نقل هتل و خدمات':
                    merge = True
                    check = True
                    continue

                if check:    
                    if merge:
                        hotel_name = texts[0]
                        {hotel_name:{text:[]}}
                        loc_info.append({hotel_name:{text:[]}})
                        key = text
                        merge = False
                        continue
                    count += 1
                    if count >= 1 and count <= 3:
                        loc_info[len(loc_info)-1][hotel_name][key].append(text) 
                    if count >= 3:
                        count = 0
                        merge = True
        for i in loc_info:
            print(i)



        






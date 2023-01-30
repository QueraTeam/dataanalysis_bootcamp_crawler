# %%
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from bs4 import BeautifulSoup
from tqdm import tqdm
from random import randint
from time import sleep
import json

def extract_hostel_data(hostel):
    result = {}
    title_tag = hostel.find('h2')
    result['title'] = ' '. join(hostel.find('p').get_text().strip().split(' ')[1:])
    result['url'] = 'https://www.jabama.com' + hostel.get('href')
    #result['rating'] = hostel.find(class_= 'rating-box-text rating-box-text__rate text-sm text-bold').get_text()
    result['city'] = hostel.select('.product-card-info span')[0].get_text().strip().split('،')[1]
    result['county'] = hostel.select('.product-card-info span')[0].get_text().strip().split('،') [0]
    result['price'] = hostel.select('.pricing span')[1].get_text().strip().split()[0]
    return result

def scrape(url):    
    results = []
    try:
        response = requests.get(url)
        print(f'HTTP response CODE: {response.status_code}')        
    except HTTPError as http_err:
        print(f'HTTP ERROR: {http_err}')
        return results
    except ConnectionError as conn_err:
        print(f'Connection ERROR: {conn_err}')
        return results
    except Timeout as timeout_err:
        print(f'Timeout ERROR: {timeout_err}')
        return results
    except RequestException as req_err:
        print(f'Request ERROR: {req_err}')
        return results

    # Parse the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find each jobs
    hostels = soup.select('.product-card')

    for count, hostel in enumerate(hostels):
        results.append(extract_hostel_data(hostel))
  
    return results


if __name__ == "__main__":
    start_page = 1
    end_page = 6
    all_results = []
    for page in tqdm(range(start_page, end_page + 1)):
        url = f'https://www.jabama.com/all-hostel?page-number={page}'
        all_results.extend(scrape(url))

        time_milliseconds = randint(500,2000)
        time_sec = 0.001 * time_milliseconds        
        sleep(time_sec)
        
    # Save the results
    with open("jabama_hostels_info.json", "w") as file:
        json.dump(all_results, file) 



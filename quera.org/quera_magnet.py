# Scraping the Quera Magnet pages
__author__ = "Parsa Abbasi"
__email__ = "parsa.abbasi1996@gmail.com"
__organization__ = "Quera"
__website__ = "https://quera.org"
__version__ = "1.0.0"
__date__ = "2023-01-06"

import requests
from bs4 import BeautifulSoup
import numpy as np
import logging
import json
from random import randint
from time import sleep
from tqdm import tqdm
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

def extract_data(job):
    result = {}

    title_tag = job.find('h2')
    # Find the title
    result['title'] = title_tag.get_text()
    # Find the link
    result['url'] = 'https://quera.org/' + title_tag.find('a').get('href')

    # Find the date
    date = job.select('.chakra-stack .css-nm8t2j span')
    result['date'] = date[0].get('title')

    # Find the company
    result['company'] = job.find(class_='chakra-text').get_text()

    # Find the location
    location = job.select('.chakra-stack .css-5ngv18 span')
    if len(location) == 1:
        result['location'] = location[0].get_text()
    else:
        result['location'] = np.nan

    details = job.select('.css-1iyteef span')
    # Find the level
    result['level'] = details[0].get_text()
    # Find the type
    result['type'] = details[1].get_text()
    # Find the salary and remote possibility
    result['salary'] = np.nan
    result['remote'] = np.nan
    if len(details) >= 3:
        if 'دورکاری' in details[2].get_text():
            result['remote'] = details[2].get_text()
        else:
            result['salary'] = details[2].get_text()
    if len(details) >= 4:
        result['remote'] = details[3].get_text()

    # Find all technologies and sub-technologies
    technologies = job.find_all(class_='css-1ljl88f')
    result['technologies'] = [tech.get_text() for tech in technologies]
    sub_technologies = job.find_all(class_='css-1suxakh')
    result['sub_technologies'] = [tech.get_text() for tech in sub_technologies]

    return result


def scrape(url, logger):
    logger.info('Starting to scrape the page [{}]'.format(url))
    
    results = []

    # Get the page
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except HTTPError as http_err:
        logger.error('HTTP error occurred: {}'.format(http_err))
        return results
    except ConnectionError as conn_err:
        logger.error('Connection error occurred: {}'.format(conn_err))
        return results
    except Timeout as timeout_err:
        logger.error('Timeout error occurred: {}'.format(timeout_err))
        return results
    except RequestException as req_err:
        logger.error('Request error occurred: {}'.format(req_err))
        return results

    # Parse the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find each jobs
    jobs = soup.select('.css-1g5o4an')

    for count, job in enumerate(jobs):
        try:
            results.append(extract_data(job))
        except:
            logger.warning('Failed to extract data from job #{}'.format(count))

    logger.info('This page scraped successfully.')
    
    return results

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(filename='quera_magnet.log', filemode='w', format='%(asctime)s %(levelname)s: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Set up the range of pages to scrape
    start_page = 1
    end_page = 15
    
    # Scrape the pages
    all_results = []
    # Loop over the pages
    for page in tqdm(range(start_page, end_page + 1)):
        # Create the url
        url = f'https://quera.org/magnet/jobs?order=high_salary&page={page}'
        # Scrape the page
        all_results.extend(scrape(url, logger))
        # Sleep for a random time to avoid being blocked
        time_milliseconds = randint(500,2000)
        time_sec = 0.001 * time_milliseconds
        logger.info('Sleeping for {} seconds'.format(time_sec))
        sleep(time_sec)
        logger.info('Woke up')

    # Save the results
    with open("quera_magnet.json", "w") as file:
        json.dump(all_results, file)
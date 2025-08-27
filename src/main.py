import sys
import os
import csv
from enum import Enum

# Add the parent directory of "src" to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from bs4 import BeautifulSoup
from src.crawls.api_crawler import APICrawler
from src.crawls.beautiful_soup_crawler import BeautifulSoupCrawler
from src.database.dao_holder import work_days_api_dao, work_days_beautifulsoup_dao
from src.service.file_service import read_urls_from_file, save_urls_to_file
from src.service.google_service import fetch_google_search_results
from src.service.proxy_service import ProxyService


def html_to_string(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.text

def convert_to_string():
    data = work_days_api_dao.find({})
    for item in data:
        item['jobDescription'] = html_to_string(item['jobDescription'])
        inserted = work_days_beautifulsoup_dao.save(item)
        print(f"Inserted: {inserted}")

def run_api_crawler(urls):
    apiCrawler = APICrawler(urls)
    try:
        apiCrawler.start()
    except Exception as e:
        print(f"Failed to start API crawler: {e}")

def run_beautiful_soup_crawler(urls):
    beautifulCrawler = BeautifulSoupCrawler(urls)
    try:
        beautifulCrawler.start()
    except Exception as e:
        print(f"Failed to start BeautifulSoup crawler: {e}")

if __name__ == '__main__':
    urls = read_urls_from_file()
    if not urls:
        proxy = ProxyService().get()['https']
        urls = fetch_google_search_results(proxy=proxy)
        save_urls_to_file(urls)
        print(f"Found {len(urls)} urls")

    run_api_crawler(urls)
    # run_beautiful_soup_crawler(urls)

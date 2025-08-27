from urllib.parse import urlparse

from googlesearch import search
from src.service.url_service import is_valid_url

# inurl:myworkdayjobs.com
SEARCH_QUERY = 'inurl:myworkdayjobs.com'


# return urls
def fetch_google_search_results(query=SEARCH_QUERY, num_pages=5, results_per_page=10, proxy=None):
    urls = set()
    try:
        sources = search(query, num_results=results_per_page * num_pages, proxy=proxy, lang='en')
        urls.update(sources)
    except Exception as e:
        print(f"An error occurred during the search: {e}")

    # remove unvalid urls
    urls = filter(is_valid_url, urls)
    return list(urls)
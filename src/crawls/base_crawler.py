from abc import ABC, abstractmethod


class BaseCrawler(ABC):
    def __init__(self, urls):
        self.urls = urls
        self.visited_urls = set()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def _crawl(self, url):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def _save_to_db(self, job_posting_infos):
        pass

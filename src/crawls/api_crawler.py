import time
from concurrent.futures import ThreadPoolExecutor

import requests
from fake_useragent import UserAgent

from src.crawls.base_crawler import BaseCrawler
from src.database.dao_holder import work_days_api_dao
from src.dto.job_posting_info_dto import JobPostingInfoDTO
from src.models.job_info import JobPostingInfo
from src.service.json_service import json_to_posting_info
from src.service.proxy_service import ProxyService
from src.service.url_service import is_valid_url, to_base_url, to_jobs_url, to_external_url, to_overview_referer, \
    to_detail_referer, subdomain_prefix


class APICrawler(BaseCrawler):
    def __init__(self, urls):
        super().__init__(urls)
        self.executors = ThreadPoolExecutor(max_workers=10)

    def start(self):
        for url in self.urls:
            print('Start crawling url=', url)
            self._crawl(url)
            # future = self.executors.submit(self._crawl, url)
            # future.result()
        # self.executors.map(self._crawl, self.urls)

    def _crawl(self, url):
        base_url = to_base_url(url)
        referer = to_overview_referer(url)
        user_agent = UserAgent(browsers=['chrome'], os=['macos'])
        headers = {"User-Agent": user_agent.chrome,
                   "Content-Type": "application/json",
                   "Accept": "application/json",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "en-US",
                   "Origin": base_url,
                   "Referer": referer,
                   "Sec-Fetch-Dest": "empty",
                   "Sec-Fetch-Mode": "cors",
                   "Sec-Fetch-Site": "same-origin"}

        offset = 0
        body = {"limit": 20, "offset": offset, "searchText": ""}
        (jobs, max_total) = self._crawl_overviews(url, headers, body)
        loop_count = int(max_total / 20)
        if max_total % 20 != 0:
            loop_count += 1

        while loop_count > 0:
            print('loop_count=', loop_count, 'offset=', offset)
            body["offset"] = offset
            offset += 20
            if jobs is not None:
                self._process_details(url, headers, jobs)
            (jobs, total) = self._crawl_overviews(url, headers, body)
            # future = self.executors.submit(self._crawl_overviews, url, headers, body)
            # (jobs, total) = future.result()
            loop_count -= 1

    def _crawl_overviews(self, url, headers, body):
        jobs_url = to_jobs_url(url)
        if not is_valid_url(jobs_url):
            print(f"Invalid url: {jobs_url}")
            return (None, None)
        # if self.visited_urls.__contains__(jobs_url):
        #     print(f"Already visited {jobs_url}")
        #     return (None, None)

        print(f"Start crawling {jobs_url}")
        response = requests.post(jobs_url, headers=headers, json=body)
        # self.visited_urls.add(jobs_url)
        if response.status_code != 200:
            print(f"Failed to crawl {jobs_url}")
            return (None, None)

        jobs = response.json()
        total = jobs["total"]
        print(f"Total jobs: {total}")
        return jobs["jobPostings"], total

    def _process_details(self, url, headers, jobs):
        job_posting_infos = []
        for job in jobs:
            try:
                if not job["externalPath"]:
                    continue
            except KeyError:
                continue

            external_path = job["externalPath"]
            reference_url = to_detail_referer(url, external_path)
            external_url = to_external_url(url, external_path)
            source = subdomain_prefix(url)

            if not is_valid_url(external_url):
                print(f"Invalid url: {external_url}")
                continue

            headers.update({"Referer": reference_url})
            if self.visited_urls.__contains__(external_url):
                print(f"Already visited {external_url}")
                continue
            job_posting_info = self._crawl_detail(external_url, headers, source)
            # future = self.executors.submit(self._crawl_detail, external_url, headers, source)
            # job_posting_info = future.result()
            if job_posting_info:
                job_posting_infos.append(job_posting_info)

        self._save_to_db(job_posting_infos)

    def _crawl_detail(self, url, headers, source) -> JobPostingInfo | None:
        try:
            response = requests.get(url, headers=headers)
            self.visited_urls.add(url)
            if response.status_code != 200:
                print(f"Failed to crawl {url} with status code {response.status_code}")
                return None
            print('Start crawling detail url=', url, 'from source =', source)
            job_info_json = response.json()
            # print('job_info_json=', job_info_json)
            time.sleep(0.25)

            return json_to_posting_info(job_info_json, source=source)
        except Exception as e:
            print(f"Failed to crawl {url} with exception {e}")
            return None

    def _save_to_db(self, job_posting_infos):
        try:
            print("Start saving to database")
            job_posting_infos_dicts = JobPostingInfoDTO.to_mongo_dicts(job_posting_infos)
            result = work_days_api_dao.save_many(job_posting_infos_dicts)
            print(f"Inserted {result.inserted_ids} job postings")
            return result.inserted_ids
        except Exception as e:
            print(f"Failed to save to database with exception {e}")
            return None

    def stop(self):
        self.executors.shutdown()
        print("Stopped crawling api")

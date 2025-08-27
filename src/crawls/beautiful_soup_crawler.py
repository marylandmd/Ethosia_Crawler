import re
import uuid

from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from src.crawls.base_crawler import BaseCrawler
from src.database.dao_holder import work_days_beautifulsoup_dao
from src.dto.job_posting_info_dto import JobPostingInfoDTO
from src.models.job_info import JobPostingInfo
from src.service.beautiful_soup_service import fetch_or_empty
from src.service.proxy_service import ProxyService
from src.service.url_service import to_base_url, subdomain_prefix


class BeautifulSoupCrawler(BaseCrawler):
    total_jobs_found_selectors = 'p[data-automation-id="jobFoundText"]'
    job_list_selectors = 'section > ul[role="list"]'
    detail_href_selectors = 'a[data-automation-id="jobTitle"]'
    next_button_selectors = 'button[data-uxi-element-id="next"]'
    detail_content_container_selectors = 'div[data-automation-id="job-posting-details"]'

    detail_title_selectors = 'h2[data-automation-id="jobPostingHeader"]'
    detail_remote_type_selectors = "div[data-automation-id='remoteType'] > dl > dd"
    detail_location_selectors = "div[data-automation-id='locations'] > dl > dd"
    detail_time_type_selectors = "div[data-automation-id='time'] > dl > dd"
    detail_posted_on_selectors = "div[data-automation-id='postedOn'] > dl > dd"
    detail_job_req_id_selectors = "div[data-automation-id='requisitionId'] > dl > dd"
    detail_job_description_selectors = "div[data-automation-id='jobPostingDescription']"

    def __init__(self, urls):
        super().__init__(urls)
        self.driver = self._fetch_chrome_driver()

    def _fetch_chrome_driver(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-application-cache')
            options.add_argument('--disable-gpu')
            options.add_argument("--disable-dev-shm-usage")
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_argument("--lang=en")
            # options.add_argument('--proxy-server={}'.format(ProxyService().get()['https']))

            # turn off browser notification
            prefs = {"credentials_enable_service": False,
                     "profile.password_manager_enabled": False}
            options.add_experimental_option("prefs", prefs)

            options.add_argument(f"user-agent={UserAgent(browsers=['chrome'], os=['macos']).chrome}")
            options.add_argument('--headless=new')  # run headless, not show browser
            service = webdriver.ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception as e:
            print(f"Failed to fetch chrome driver: {e}")
            return None

    def start(self):
        [self._crawl(url) for url in self.urls]

    def _crawl(self, url):
        base_url = to_base_url(url)
        print(f"Start crawling {url}")
        self._open_url(url)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        total_jobs = self._fetch_total_jobs_found(soup)

        # for 20 items per page
        offset = 0
        while offset < total_jobs:
            external_urls = self._crawl_hrefs(soup)
            self._process_details(base_url, external_urls)
            offset += 20

            next_page = self._next_page()
            if next_page:
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            else:
                break

    def _next_page(self):
        nextPageButton = self.driver.find_element(By.CSS_SELECTOR, self.next_button_selectors)
        if nextPageButton:
            nextPageButton.click()
            self.driver.implicitly_wait(2)
            return True
        return False

    # return list href of jobs
    def _crawl_hrefs(self, soup):
        jobs = []
        details = soup.select(self.detail_href_selectors)

        for detail in details:
            try:
                jobs.append(detail['href'])
            except IndexError:
                print("No href found.")
                continue

        return jobs

    def _open_url(self, url):
        # if self.visited_urls.__contains__(url):
        #     print(f"Already visited {url}")
        #     return
        self.driver.get(url)
        self.visited_urls.add(url)
        # wait until page loaded
        (WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, self.job_list_selectors))))

    def _fetch_detail_response(self, url):
        # if self.visited_urls.__contains__(url):
        #     print(f"Already visited {url}")
        #     return
        local_driver = self._fetch_chrome_driver()
        local_driver.get(url)
        self.visited_urls.add(url)
        (WebDriverWait(local_driver, 10)
         .until(EC.presence_of_element_located((By.CSS_SELECTOR, self.detail_content_container_selectors))))
        return local_driver.page_source

    # return total jobs found, int value
    def _fetch_total_jobs_found(self, soup):
        try:
            total_jobs_found = soup.select_one(self.total_jobs_found_selectors)
            if not total_jobs_found:
                print("fetch_total_jobs_found failed")
                return 0

            pattern = r'\d+'
            int_total_jobs_found = int(re.findall(pattern, total_jobs_found.text)[0])
            return int_total_jobs_found
        except IndexError:
            print("No jobs found.")
            return 0
        except ValueError:
            print("Could not convert job count to integer.")
            return 0

    def _process_details(self, base_url, external_urls):
        job_posting_infos = []
        for external_url in external_urls:
            full_url = f"{base_url}{external_url}"
            print(f"Start crawling {full_url}")
            response = self._fetch_detail_response(full_url)
            detail_soup = BeautifulSoup(response, 'html.parser')
            job_posting_info = self._crawl_detail(detail_soup, external_url, subdomain_prefix(base_url))
            if job_posting_info:
                job_posting_infos.append(job_posting_info)

        self._save_to_db(job_posting_infos)

    def _crawl_detail(self, soup, external_link, source) -> JobPostingInfo | None:
        try:
            title = fetch_or_empty(soup, self.detail_title_selectors)
            remote_type = fetch_or_empty(soup, self.detail_remote_type_selectors)
            location = fetch_or_empty(soup, self.detail_location_selectors)
            time_type = fetch_or_empty(soup, self.detail_time_type_selectors)
            posted_on = fetch_or_empty(soup, self.detail_posted_on_selectors)
            job_req_id = fetch_or_empty(soup, self.detail_job_req_id_selectors)
            job_description = fetch_or_empty(soup, self.detail_job_description_selectors)
            return JobPostingInfo(id=str(uuid.uuid4()),
                                  title=title,
                                  jobDescription=job_description,
                                  location=location,
                                  postedOn=posted_on,
                                  startDate=None,
                                  timeType=time_type,
                                  jobReqId=job_req_id,
                                  jobPostingId='',
                                  jobPostingSiteId='',
                                  country=location,
                                  canApply=True,
                                  jobRequisitionLocation=None,
                                  remoteType=remote_type,
                                  externalUrl=external_link,
                                  jobSource=source,
                                  hiringOrganization='')
        except Exception as e:
            print(f"Failed to crawl detail with exception {e}")
            return None

    def _save_to_db(self, job_posting_infos):
        try:
            job_posting_infos_dicts = JobPostingInfoDTO.to_mongo_dicts(job_posting_infos)
            result = work_days_beautifulsoup_dao.save_many(job_posting_infos_dicts)
            print(f"Inserted {result.inserted_ids} job postings")
            return result.inserted_ids
        except Exception as e:
            print(f"Failed to save to database with exception {e}")
            return None

    def stop(self):
        self.driver.quit()
        print("Stop crawling beautiful soup")

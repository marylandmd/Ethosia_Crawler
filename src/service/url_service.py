import re
from urllib.parse import urlparse

URL_REGEX = re.compile(r'^(?:http|ftp)s?://'  # http:// or https://
                       r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)*myworkdayjobs\.com|'
                       r'localhost|'  # localhost...
                       r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
                       r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
                       r'(?::\d+)?'  # optional port
                       r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def domain(url: str) -> str:
    return urlparse(url).netloc


# Get the first part of the domain (subdomain prefix, like 'absa')
def subdomain_prefix(url: str) -> str:
    return domain(url).split('.')[0]


def scheme(url: str) -> str:
    return urlparse(url).scheme


def path(url: str) -> str:
    return urlparse(url).path.removesuffix('/')


def is_valid_url(url: str) -> bool:
    return bool(re.match(URL_REGEX, url))


def to_base_url(url: str) -> str:
    return f"{scheme(url)}://{domain(url)}"


# MARK: - Process URLs
API_PATH_PREFIX = "wday/cxs"
PATH_JOBS = "jobs"
LANG = "en-US"


def to_jobs_url(url: str) -> str:
    return f"{to_base_url(url)}/{API_PATH_PREFIX}/{subdomain_prefix(url)}{path(url)}/{PATH_JOBS}"


def to_external_url(url: str, external_path: str) -> str:
    return f"{to_base_url(url)}/{API_PATH_PREFIX}/{subdomain_prefix(url)}{path(url)}{external_path}"


def to_overview_referer(url: str) -> str:
    return f"{to_base_url(url)}/{LANG}{path(url)}"


def to_detail_referer(url: str, external_path: str) -> str:
    # replace 'job' to en-US/subdomain_prefix/details
    external_path_process = external_path.replace('job', f'{LANG}/{subdomain_prefix(url)}/details')
    return f"{to_base_url(url)}{external_path_process}"

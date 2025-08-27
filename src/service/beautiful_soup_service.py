def fetch_or_empty(soup, selector):
    element = soup.select_one(selector)
    return element.text if element else ''

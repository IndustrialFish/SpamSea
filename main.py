import urllib
import time

import requests


def check_website_status(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
        'Accept-Language': 'en-gb',
        'referer': 'https://google.com'}

    request_response = requests.get(url, headers)
    status_code = request_response.status_code
    website_is_up = status_code == 200
    return status_code


while True:
    print(check_website_status("https://opensea.io/collection/cryptopunk-50"))
    time.sleep(1)

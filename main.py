import urllib
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv


def check_website_status(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
        'Accept-Language': 'en-gb'}

    request_response = requests.get(url, headers=headers)
    status_code = request_response.status_code
    return status_code


def check_number_variants(collectionName):
    for x in range(10000):

        modified_url = 'https://opensea.io/collection/' + collectionName + '-' + str(x)

        status_code = check_website_status(modified_url)

        if status_code == 200:

            with open('Fraudulent Collections.csv', 'a+') as f:
                f.write(modified_url)

            print('200 :' + modified_url)


check_number_variants("cryptopunk")

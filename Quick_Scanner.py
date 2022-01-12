# General Libraries

import requests
from requests import Session
from csv import writer


def check_website_status(url):  # This function will return the status code of a website.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
        'Accept-Language': 'en-gb'}
    s = Session()
    s.headers.update(headers)
    request_response = s.get(url, headers=headers)
    status_code = request_response.status_code
    return status_code


with open('ManualCheck.csv', 'a', newline='') as write_obj:
    csv_writer = writer(write_obj)
    row = ["URL", "Items", "Creator", "11/01/21"]
    csv_writer.writerow(row)
for x in range(25000):
    modified_url = 'https://opensea.io/collection/' + str(x)
    status_code = check_website_status(modified_url)
    print(str(status_code) + " " + modified_url)
    if status_code == 200:
        r = requests.get(
            'https://api.opensea.io/api/v1/assets?order_direction=desc&offset=0&limit=20&collection=https://opensea.io/collection/cool-cats-nft-' + str(x))
        print(str(status_code) + " " + modified_url)
        length = len(r.json()['assets'])
        if length != 0:
            created_by = r.json()['assets'][0]['creator']['user']['username']
            with open('ManualCheck.csv', 'a', newline='') as write_obj:
                csv_writer = writer(write_obj)
                row = [modified_url, length, created_by]
                csv_writer.writerow(row)
            print(modified_url + " " + str(length) + " " + str(created_by))
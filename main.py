import os
import urllib
import time
import bs4
import pandas as pd
from bs4 import BeautifulSoup
import requests, json
from csv import writer
from datetime import datetime
from urllib.request import urlopen, Request
from os.path import basename
import re
import shutil



def check_website_status(url):  # This function will return the status code of a website.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
        'Accept-Language': 'en-gb'}

    request_response = requests.get(url, headers=headers)
    status_code = request_response.status_code
    return status_code


def check_number_variants(collectionName):  # Iterate using the following convention https://opensea.io/collection/{
    # collectionName}-{x}

    with open('Suspect Collections 2.csv', 'a', newline='') as write_obj:
        csv_writer = writer(write_obj)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        row = ['Time', 'URL', 'Created By', 'Image URL']
        csv_writer.writerow(row)

    for x in range(10000):

        modified_url = 'https://opensea.io/collection/' + collectionName + '-' + str(x)
        status_code = check_website_status(modified_url)

        if status_code == 200:

            r = requests.get(
                'https://api.opensea.io/api/v1/assets?order_direction=desc&offset=0&limit=20&collection=' + collectionName + '-' + str(
                    x))

            print(r.json())

            try:
                image_url = r.json()['assets'][0]['image_url']
            except:
                image_url = "Failed to retrieve image"

            try:
                created_by = r.json()['assets'][0]['creator']['user']['username']
            except:
                created_by = "Failed to retrieve creator"

            with open('Suspect Collections 2.csv', 'a', newline='') as write_obj:
                csv_writer = writer(write_obj)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                row = [current_time, modified_url, created_by, image_url]
                csv_writer.writerow(row)


    print('---------------------')
    print('All Collections Found')
    print('---------------------')


print('ScamSea Running...')
print('------------------')
print('Checking for collections...')

check_number_variants("cryptopunk")



# PLAN
# -----------------------------#
# Find images on page
# Download images
# Download all Collection images
# Check Current against original
# Create Report Ticket with info and csv

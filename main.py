# General Libraries

import urllib
import requests, json
from csv import writer
from datetime import datetime
from urllib.request import urlopen, Request

# OpenCV Libraries

from skimage.metrics import structural_similarity as compare_ssim
import argparse
import imutils
import cv2

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
        row = ['Time', 'URL', 'Created By', 'Image URL', 'CopyMint Detected']
        csv_writer.writerow(row)


    with open('Empty_collection.csv', 'a', newline='') as write_obj:
        csv_writer = writer(write_obj)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        row = ['Time', 'URL', 'Created By', 'Image URL', 'CopyMint Detected']
        csv_writer.writerow(row)

    for x in range(10000):

        modified_url = 'https://opensea.io/collection/' + collectionName + '-' + str(x)
        status_code = check_website_status(modified_url)

        if status_code == 200:

            r = requests.get(
                'https://api.opensea.io/api/v1/assets?order_direction=desc&offset=0&limit=20&collection=' + collectionName + '-' + str(
                    x))

            print("Scanning: " + collectionName + "-" + str(x))

            try:
                image_url = r.json()['assets'][0]['image_url']
            except:
                image_url = "Failed to retrieve image"
            try:
                created_by = r.json()['assets'][0]['creator']['user']['username']
            except:
                created_by = "Empty Collection"

            if image_url == "Failed to retrieve image":
                with open('Empty_collection.csv', 'a', newline='') as write_obj:
                    csv_writer = writer(write_obj)
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    row = [current_time, modified_url, created_by, image_url, "FALSE"]
                    csv_writer.writerow(row)
            else:

                try:
                    urllib.request.urlretrieve(image_url, "images/duplicate.png")
                except:
                    None

                for y in range(10000):

                    y = '{0:04}'.format(y)

                    try:
                        dim = (336, 336)
                        duplicate = cv2.imread("images/duplicate.png")
                        resized_duplicate = cv2.resize(duplicate, dim, interpolation=cv2.INTER_AREA)
                        original = cv2.imread("images/cryptopunks/" + str(y) + ".png")

                        gray_image = cv2.cvtColor(duplicate, cv2.COLOR_BGR2GRAY)
                        histogram = cv2.calcHist([gray_image], [0],
                                                 None, [256], [0, 256])

                        gray_image1 = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
                        histogram1 = cv2.calcHist([gray_image1], [0],
                                                  None, [256], [0, 256])

                        c1 = 0

                        # Euclidean Distance between data1 and test
                        i = 0
                        while i < len(histogram) and i < len(histogram1):
                            c1 += (histogram[i] - histogram1[i]) ** 2
                            i += 1
                        c1 = c1 ** (1 / 2)

                        if c1 < 10000:
                            with open('Suspect Collections 2.csv', 'a', newline='') as write_obj:
                                csv_writer = writer(write_obj)
                                now = datetime.now()
                                current_time = now.strftime("%H:%M:%S")
                                row = [current_time, modified_url, created_by, image_url, "CopyMint: Punk#" + str(y) ]
                                csv_writer.writerow(row)
                                print(row)
                            break

                        if y == 10000 & c1 > 10000:

                            with open('Suspect Collections 2.csv', 'a', newline='') as write_obj:
                                csv_writer = writer(write_obj)
                                now = datetime.now()
                                current_time = now.strftime("%H:%M:%S")
                                row = [current_time, modified_url, created_by, image_url, "No Match" ]
                                csv_writer.writerow(row)
                                print(row)
                            break

                    except:
                         None

    print('---------------------')
    print('All Collections Found')
    print('---------------------')

print('---------------')
print('ScamSea Running')
print('---------------')
print('Scanning Collections...')

check_number_variants("cryptopunk")


# General Libraries

import urllib
import requests, json
from csv import writer
from datetime import datetime
from urllib.request import urlopen
from requests import Session

# OpenCV Libraries

from skimage.metrics import structural_similarity as compare_ssim
import argparse
import imutils
import cv2
from PIL import Image


def check_website_status(url):  # This function will return the status code of a website.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
        'Accept-Language': 'en-gb'}
    s = Session()
    s.headers.update(headers)
    request_response = s.get(url, headers=headers)
    status_code = request_response.status_code
    return status_code


def check_number_variants(collectionName, originalCollection):
    with open('Suspect Collections.csv', 'a', newline='') as write_obj:
        csv_writer = writer(write_obj)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        row = ['Time', 'collectionName', 'URL', 'Created By', 'Image URL', 'CopyMint Detected']
        csv_writer.writerow(row)

    for x in range(10000):

        modified_url = 'https://opensea.io/collection/' + collectionName + '-' + str(x)
        status_code = check_website_status(modified_url)
        print(str(status_code) + " | Scanning: " + collectionName + "-" + str(x))

        if status_code == 200:

            r = requests.get(
                'https://api.opensea.io/api/v1/assets?order_direction=desc&offset=0&limit=20&collection=' + collectionName + '-' + str(
                    x))

            length = len(r.json()['assets'])

            if length > 10:
                length = 10

            if length != 0:

                for z in range(length):

                    image_url = r.json()['assets'][z]['image_url']
                    created_by = r.json()['assets'][z]['creator']['user']['username']
                    urllib.request.urlretrieve(image_url, "images/duplicate.png")

                    im = Image.open("images/duplicate.png")
                    rgb_im = im.convert('RGB')
                    rgb_im.save('images/duplicate.jpeg')

                    for y in range(10000):

                        y = '{0:04}'.format(y)

                        try:
                            dim = (336, 336)
                            duplicate = cv2.imread("images/duplicate.jpeg")
                            original = cv2.imread("images/" + originalCollection + "/" + str(y) + ".png")

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

                        except:
                            print("Error Processing Image")

                        print(collectionName + "-" + str(x) + " | " + str(z+1) + "/" + str(length) + " - " + str(y) + "/9999 - " + str(c1))

                        if c1 < 10000:
                            with open('Suspect Collections.csv', 'a', newline='') as write_obj:
                                csv_writer = writer(write_obj)
                                now = datetime.now()
                                current_time = now.strftime("%H:%M:%S")
                                row = [current_time, collectionName, modified_url, created_by, image_url,
                                       "CopyMint: " + originalCollection + "#" + str(y)]
                                csv_writer.writerow(row)
                                print(row)
                            break

    print('---------------------')
    print(collectionName + " Scan Complete")
    print('---------------------')


print('---------------')
print('ScamSea Running')
print('---------------')
print('Scanning Collections...')

collection_list =[['punk', 'cryptopunks'], ['cryptopunk', 'cryptopunks'], ['cryptopunks', 'cryptopunks'], ['punks', 'cryptopunks'], ['crypt0punks', 'cryptopunks'] ]

for q in collection_list:

    check_number_variants(q[0], q[1])

print('------------------------')
print("Collection Scan Complete")
print('------------------------')

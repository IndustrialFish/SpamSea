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
        row = ['Time', 'URL', 'Created By', 'Image URL']
        csv_writer.writerow(row)
        print('Added field titles to CSV')
        print(row)

    for x in range(10000):

        modified_url = 'https://opensea.io/collection/' + collectionName + '-' + str(x)
        status_code = check_website_status(modified_url)

        if status_code == 200:

            r = requests.get(
                'https://api.opensea.io/api/v1/assets?order_direction=desc&offset=0&limit=20&collection=' + collectionName + '-' + str(
                    x))

            try:
                image_url = r.json()['assets'][0]['image_url']
            except:
                image_url = "Failed to retrieve image"
            try:
                created_by = r.json()['assets'][0]['creator']['user']['username']
            except:
                created_by = "Empty Collection"

            if image_url == "Failed to retrieve image":
                with open('empty_collection.csv', 'a', newline='') as write_obj:
                    csv_writer = writer(write_obj)
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    row = [current_time, modified_url, created_by, image_url]
                    csv_writer.writerow(row)
                    print(row)
            else:
                with open('Suspect Collections 2.csv', 'a', newline='') as write_obj:
                    csv_writer = writer(write_obj)
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    row = [current_time, modified_url, created_by, image_url]
                    csv_writer.writerow(row)
                    print(row)

            for y in range(10000):

                y = '{0:04}'.format(y)

                try:
                    urllib.request.urlretrieve(image_url, "images/duplicate.png")
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

                    if c1 == 0:
                        print("Matches Punk" + str(y))

                except:
                    None

                # # 1) Check if 2 images are equals
                # if original.shape == duplicate.shape:
                #     print("The images have same size and channels")
                # difference = cv2.subtract(original, duplicate)
                # b, g, r = cv2.split(difference)
                # if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                #     print("The images are completely Equal")
                # if original.shape != duplicate.shape:
                #     print("Shape is different")
                # if cv2.countNonZero(b) != 0 and cv2.countNonZero(g) != 0 and cv2.countNonZero(r) != 0:
                #     print("Non Zero is not equal")

            # for y in range(10000):
            #     y = '{0:04}'.format(y)
            #     original = cv2.imread("images/" + str(y) + ".png")
            #     duplicate = cv2.imread("images/duplicate.png")
            #
            #     cv2.imshow("Original", original)
            #     cv2.imshow("Duplicate", duplicate)
            #
            #     # 1) Check if 2 images are equals
            #     if original.shape == duplicate.shape:
            #         print("The images have same size and channels")
            #     difference = cv2.subtract(original, duplicate)
            #     b, g, r = cv2.split(difference)
            #     if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            #         print("The images are completely Equal")
            #     if original.shape != duplicate.shape:
            #         print("Shape is different")
            #     if cv2.countNonZero(b) != 0 and cv2.countNonZero(g) != 0 and cv2.countNonZero(r) != 0:
            #         print("Non Zero is not equal")

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

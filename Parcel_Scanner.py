from csv import writer
from requests import Session


def check_website_status(url):  # This function will return the status code of a website.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15'}
    s = Session()
    s.headers.update(headers)
    request_response = s.get(url, headers=headers)
    status_code = request_response.status_code
    return status_code


with open('parcel.csv', 'a', newline='') as write_obj:
    csv_writer = writer(write_obj)
    row = ['URL', 'Status Code']
    csv_writer.writerow(row)

for x in range(26, 999):
    print("parcel" + "-" + str(x) + "-" + "Y" )
    for y in range(999):
        modified_url = 'https://opensea.io/collection/' + "parcel" + "-" + str(x) + "-" + str(y)
        status_code = check_website_status(modified_url)
        if status_code == 200:
            print(str(status_code) + " | Scanning: " + modified_url)
            with open('parcel.csv', 'a', newline='') as write_obj:
                csv_writer = writer(write_obj)
                row = [modified_url, status_code]
                csv_writer.writerow(row)


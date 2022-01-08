import urllib

def check_website_status(url):
    status_code = urllib.request.urlopen(url).getcode()
    website_is_up = status_code == 200



import requests
import os
from selectorlib import Extractor

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
e = Extractor.from_yaml_file(__location__+'/keys.yml')
print (e)

  
headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    # You may want to change the user agent if you get blocked
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'https://www.makemytrip.com',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}
url='https://www.makemytrip.com/flight/search?tripType=1&itinerary=COK-BOM-18/10/2021&paxType=A-1_C-0_I-0&cabinClass=E'
# Download the page using requests
print("Downloading %s"%url)
r = requests.get(url, headers=headers)
print (r)
#r = requests.get(url)
# Pass the HTML of the page and create 
print (e.extract(r.text,base_url=url))
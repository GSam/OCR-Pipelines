from lxml import etree
import requests

TRUCKOMETER_URL = 'https://www.anz.co.nz/about-us/economic-markets-research/truckometer/'
contents = requests.get(TRUCKOMETER_URL)

parser.etree.HTMLParser()
etree.fromstring(content.text, parser)

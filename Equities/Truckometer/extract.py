from lxml import etree
import requests
import urlparse

TRUCKOMETER_URL = 'https://www.anz.co.nz/about-us/economic-markets-research/truckometer/'
content = requests.get(TRUCKOMETER_URL)

parser = etree.HTMLParser()
tree = etree.fromstring(content.text, parser)

results = tree.xpath("//a[re:match(@href, 'ANZ-Truckometer-[\\d]+.pdf')]",
                     namespaces={"re": "http://exslt.org/regular-expressions"})

print 'URL available:'
for url in results:
    print urlparse.urljoin(TRUCKOMETER_URL, url.attrib['href'])

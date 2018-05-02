from lxml import etree
import requests
import urlparse
import urllib
import re, os, sys

num_to_parse = -1
if len(sys.argv) > 1:
    num_to_parse = int(sys.argv[1])

TRUCKOMETER_URL = 'https://www.anz.co.nz/about-us/economic-markets-research/truckometer/'
content = requests.get(TRUCKOMETER_URL)

parser = etree.HTMLParser()
tree = etree.fromstring(content.text, parser)

results = tree.xpath("//a[re:match(@href, 'ANZ-Truckometer-[\\d]+.pdf')]",
                     namespaces={"re": "http://exslt.org/regular-expressions"})

files = []
urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'

print 'URL available:'
for url in results:
    print urlparse.urljoin(TRUCKOMETER_URL, url.attrib['href'])

    filename = re.search('ANZ-Truckometer-[\\d]+.pdf', url.attrib['href']).group(0)
    files.append(filename)

    if os.path.exists(filename):
        continue

    urllib.urlretrieve(urlparse.urljoin(TRUCKOMETER_URL, url.attrib['href']), filename)

for f in reversed(sorted(files)):
    if num_to_parse == 0:
        break

    num_to_parse -= 1

    # So far the appendix always exists on page 3
    PAGE_NUM = 3
    
    output, _ = subprocess.Popen(['pdfgrep', '-n', 'APPENDIX', f],
                                 stdout=subprocess.PIPE).communicate()
    
    if ":" in output:
        PAGE_NUM = int(output.split(':')[0])
    
    output, _ = subprocess.Popen(['pdftotext', f,
                                  '-f', '3', '-l', '3', '-raw',  '-'], 
                                 stdout=subprocess.PIPE).communicate()
    
    # extract using convert ... pdf[3] image.png -crop 600x400+0x600
    # capture2text_cli ... extract output

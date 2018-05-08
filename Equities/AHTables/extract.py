import os
import sys
import subprocess
import ah_image
import urlparse
import urllib
import tempfile
import shutil

url = os.environ.get("AHTABLEURL")

if url is None:
    print("Please set the AHTABLEURL environment variable")
    sys.exit(0)

if len(sys.argv) != 3:
    print("You must supply two arguments")

dirpath = tempfile.mkdtemp()

url = url.format(sys.argv[1], sys.argv[2])
print(url)

temporary_file = os.path.join(dirpath, 'fetch.pdf')

urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'
urllib.urlretrieve(url, temporary_file)

output_gs = os.path.join(dirpath, 'pdf_to_png.png')

output, _ = subprocess.Popen(['gs', '-s', 'DEVICE=pnggray', '-r', '600', '-g',
                              '2900x3235', '-o', output_gs, '-c',
                              '<</Install {-220 -170 translate}>> setpagedevice',
                              '-f', input_file],
                             stdout=subprocess.PIPE).communicate()

output_file = os.path.join(dirpath, 'pre_processed.png')

output, _ = subprocess.Popen(['convert', '-white-threshold', '60%', '-colorspace',
                              'sRGB', '-type', 'truecolor', output_gs,
                              'PNG32:{}'.format(output_file)],
                             stdout=subprocess.PIPE).communicate()

ah_image.process_image(output_file)

shutil.rmtree(dirpath)

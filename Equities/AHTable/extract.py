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

output, _ = subprocess.Popen(['gs', '-sDEVICE=pnggray', '-r600',
                              '-g2900x3235', '-o', output_gs, '-c',
                              '<</Install {-220 -170 translate}>> setpagedevice',
                              '-f', temporary_file],
                             stdout=subprocess.PIPE).communicate()

output_file = os.path.join(dirpath, 'pre_processed.png')

output, _ = subprocess.Popen(['convert', '-white-threshold', '60%', '-colorspace',
                              'sRGB', '-type', 'truecolor',
                              '-fill', 'white', '-stroke', 'white',
                              '-strokewidth', '5',
                              '-draw', 'line 0 1942 2900 1942',
                              '-draw', 'line 0 1441 2900 1441',
                              '-draw', 'line 0 1558 2900 1558',
                              '-draw', 'line 0 1825 2900 1825',
                              output_gs,
                              'PNG32:{}'.format(output_file)],
                             stdout=subprocess.PIPE).communicate()

ah_image.process_image(output_file, scale=0.8)

shutil.rmtree(dirpath)

import os
import sys
import subprocess
import ah_image

url = os.environ.get("AHTABLEURL")

if url is None:
    print("Please set the AHTABLEURL environment variable")
    sys.exit(0)

if len(sys.argv) != 3:
    print("You must supply two arguments")

url = url.format(sys.argv[1], sys.argv[2])

# extract using convert ... pdf image.png -crop 600x400+0x600
# convert /tmp/tester.png -set colorspace gray - | convert -white-threshold 60% - /tmp/tester1.png
# Capture2Text_CLI -i test.png --scale-factor=5 --blacklist=~
# gs -sDEVICE=pnggray -r1600  -o image.png AHTABLEURL
# gs -sDEVICE=pnggray -r600 -g2900x3235 -o image.png -c -c "<</Install {-220 -170 translate}>> setpagedevice" -f  AHTABLEURL

filename = ''
ah_image.process_image(filename)

print(url)

import os
import sys

url = os.environ.get("AHTABLEURL")

if url is None:
    print("Please set the AHTABLEURL environment variable")
    sys.exit(0)
    
if len(sys.argv) != 3:
    print("You must supply two arguments")

url = url.format(sys.argv[1], sys.argv[2])
print(url)

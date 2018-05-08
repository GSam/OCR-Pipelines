import subprocess

def process_image(filename):
    output, _ = subprocess.Popen(['Capture2Text_CLI'],
                                  stdout=subprocess.PIPE).communicate()

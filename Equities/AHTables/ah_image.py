import subprocess

def process_image(filename):
    output, _ = subprocess.Popen(['Capture2Text_CLI', '-i', filename,
                                  '--blacklist', '~', '--scale-factor', '1'],
                                  stdout=subprocess.PIPE).communicate()
    # interpret output here
    return ''

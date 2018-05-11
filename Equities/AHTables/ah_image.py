import subprocess

def process_image(filename):
    output, _ = subprocess.Popen(['./Capture2Text_CLI', '-platform',
                                  'offscreen', '-i', filename,
                                  '--blacklist', '~|\\V', '--scale-factor', '1'],
                                  stdout=subprocess.PIPE).communicate()
    # interpret output here
    print output
    return output

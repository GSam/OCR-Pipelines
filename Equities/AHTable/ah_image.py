import subprocess

def process_image(filename, scale=1.0):
    output, _ = subprocess.Popen(['./Capture2Text_CLI', '-platform',
                                  'offscreen', '-i', filename,
                                  '--blacklist', '~|\\V', '--scale-factor', str(scale)],
                                  stdout=subprocess.PIPE).communicate()
    # interpret output here
    print output
    return output

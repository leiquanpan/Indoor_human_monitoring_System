 # This file is for periodically capture image and then publish to AWS IoT
# There are three parameters that needs to be provided.
# -p: period    The period to capture image
# -t: times     How manys times you want to capture

import argparse
from picamera import PiCamera
from time import sleep
import time
from datetime import datetime
import subprocess

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--period", action="store", required=True, dest="period", help="The period you want to set")
parser.add_argument("-t", "--times", action="store", required=True, dest="times", help="How many times you want to capture")

args = parser.parse_args()
period = args.period
times = args.times

#Camera settings
camera = PiCamera()
camera.resolution=(1920,1080)
camera.framerate = 15

#Start periodically capture image, send them to AWS IoT
loopCount = 0
while loopCount < times:
    loopCount += 1
    timestamp = str(time.time())
    time_count = timestamp + "_Number_" + str(loopCount)
    camera.capture('/home/pi/CSE521/pictures/test_%s.jpg' % time_count)
    filePath = "/home/pi/CSE521/pictures/test_" + time_count + ".jpg"
    interval = float(period)/2
    command = "python /home/pi/CSE521/publisher/publisher.py -e apj4uko2zpf4y.iot.us-west-2.amazonaws.com -r ../IoT_CERT/root-CA -c ../IoT_CERT/certificate.pem.crt -k ../IoT_CERT/private.pem.key -m publish -t aws/things/Image_broker_01/shadow/update -M " + filePath + " -i " + str(interval)
    subprocess.call(command,shell = True)
    sleep(float(period))

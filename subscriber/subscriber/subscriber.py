# Author: lpan22@wustl.edu
# This file is for reveicing image from AWS IoT and store them into local file system, and forward them to Face-recognition file to get the results

import paho.mqtt.client as paho
import os
import socket
import ssl
import json
from time import sleep
from random import randint
from datetime import datetime
import argparse
import cv2
import numpy as np
import time
import subprocess

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

def on_message(client, userdata, msg):
    timestamp = str(time.time())
    filePath = os.getcwd() + "/../pictures/received_picture_" + timestamp + ".jpeg"
    image = np.asarray(bytearray(msg.payload),dtype="uint8")
    decimg = cv2.imdecode(image, 1)
    cv2.imwrite(filePath,decimg)
    print("Received a photo, and stored time into %s" % filePath)
    print("start processing")
    command = "python3 ../face_rocoginition/faceCount.py -f " + filePath + " -e ../processed_pictures"
    subprocess.call(command,shell = True)
    print("end processing")

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="awsEndpoint", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")

args = parser.parse_args()
awsEndpoint = args.awsEndpoint
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
topic = args.topic

# Create an mqtt Client Object: mqttc
# Bind the callback method on specific event
mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

awsPort     = 8883
qos         = 0

mqttc.tls_set(rootCAPath, certfile = certificatePath, keyfile = privateKeyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awsEndpoint, awsPort, keepalive=60)
mqttc.subscribe(topic , qos)
mqttc.loop_start()

while 1==1:
    sleep(2)

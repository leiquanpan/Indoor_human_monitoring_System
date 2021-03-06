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

#initialize hash_map
print("Initialize dictions")
hash_map = {}

#bytes to int implementation
def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result


#processing first part of image, insert into hash_map
def process_first_part(random_number, image_data, sequence):
    if sequence == 0:
        hash_map[random_number] = image_data
        print("add into hash map")

def process_following_part(random_number, image_data, sequence):
    if(random_number not in hash_map.keys()):
        print("There is no first map matching, drop it")
        return
    
    im_bytes = hash_map[random_number]
    pre_sequence = bytes_to_int(im_bytes[:1])
    if(sequence - pre_sequence != 1):
        print("Lost packet, drop whole")
        hash_map.pop(random_number)
        return

    hash_map[random_number] = image_data[:1] + im_bytes[1:] + image_data[1:]
    print("add more")

#processing second part of image, if match generate
def process_end_part(random_number, image_data, sequence):
    if(random_number not in hash_map.keys()):
        print("There is no first map matching, drop it")
        return
    
    first_half = hash_map[random_number]
    pre_sequence = bytes_to_int(first_half[:1])
    if(sequence - pre_sequence != 1):
        print("Lost packet, drop whole")
        hash_map.pop(random_number)
        return

    hash_map.pop(random_number)
    whole_image = first_half[1:] + image_data[1:]

    #begin to grnerate image
    timestamp = str(time.time())
    filePath = os.getcwd() + "/../pictures/received_picture_" + timestamp + ".jpeg"
    image = np.asarray(whole_image,dtype="uint8")
    decimg = cv2.imdecode(image, 1)
    cv2.imwrite(filePath,decimg)
    print("Received a photo, and stored time into %s" % filePath)
    print("start processing")
    command = "python3 ../face_rocoginition/faceCount.py -f " + filePath + " -e ../processed_pictures"
    subprocess.call(command,shell = True)
    print("end processing")

def process_whole_part(image_data):
    #begin to grnerate image
    timestamp = str(time.time())
    filePath = os.getcwd() + "/../pictures/received_picture_" + timestamp + ".jpeg"
    image = np.asarray(image_data,dtype="uint8")
    decimg = cv2.imdecode(image, 1)
    cv2.imwrite(filePath,decimg)
    print("Received a photo, and stored time into %s" % filePath)
    print("start processing")
    command = "python3 ../face_rocoginition/faceCount.py -f " + filePath + " -e ../processed_pictures"
    subprocess.call(command,shell = True)
    print("end processing")

#connect callback
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))


#new_function of message callback
def on_message(client, userdata, msg):
    #start to analysis data,analyze ID,random_id,msg_data
    input_msg = bytearray(msg.payload)
    length = len(input_msg)
    
    identity = bytes_to_int(input_msg[:1])
    print("Identity is " + str(identity))
    if (identity == 3):
        process_whole_part(input_msg[1:])
        return

    sequence = bytes_to_int(input_msg[1:2])
    print("Sequence is " + str(sequence))    
    random_id = bytes_to_int(input_msg[length-2:length])
    half_image_data = input_msg[1:length-2]
    
    if (identity == 0):
        process_first_part(random_id, half_image_data, sequence)
    elif (identity == 1):
        process_following_part(random_id, half_image_data, sequence)
    elif (identity == 2):
        process_end_part(random_id, half_image_data, sequence)



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

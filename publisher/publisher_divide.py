'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import cv2
import random

AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
                    help="Operation modes: %s"%str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                    help="Message to publish")
parser.add_argument("-i", "--interval", action="store", dest="interval", default="2",
                    help="waiting for publish to finish")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic
interval = args.interval
path = args.message

#parameters for identity
start = 0
middle = 1
end = 2
whole = 3

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, 443)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT

myAWSIoTMQTTClient.connect()
if args.mode == 'both' or args.mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while loopCount < 1:
    if args.mode == 'both' or args.mode == 'publish':
        message = {}
        path = args.message
        img = cv2.imread(path,1)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),100]
        result, encimg = cv2.imencode('.jpg', img, encode_param)
        #have bytearray
        original_graph = bytearray(encimg)
        length = len(original_graph)
        start = 0
        sequence = 0
        
        #add random number
        random_number = random.randint(1,1024)
        
        if length >= 100*1024:
            first_part = original_graph[start:start + 100*1024]
            #add identification
            first_part = start.to_bytes(1, byteorder='big') + sequence.to_bytes(1, byteorder='big') + first_part
            first_part = first_part + random_number.to_bytes(2, byteorder='big')
            myAWSIoTMQTTClient.publish(topic, bytearray(first_part), 1)
            print("Published first half of message " + str(loopCount))
        else:
            original_graph = whole.to_bytes(1, byteorder='big') + original_graph
            myAWSIoTMQTTClient.publish(topic, bytearray(original_graph), 1)
            print("Published the whole message " + str(loopCount))
            continue
        
        length = length - 100*1024
        start = 100*1024
        sequence = sequence + 1
        
        while length >= 100*1024:
            following_part = original_graph[start:start + 100*1024]
            following_part = middle.to_bytes(1, byteorder='big') + sequence.to_bytes(1, byteorder='big') + following_part
            following_part = following_part + random_number.to_bytes(2, byteorder='big')
            myAWSIoTMQTTClient.publish(topic, bytearray(following_part), 1)
            print("Published following half of message " + str(loopCount))
            length = length - 100*1024
            start = start + 100*1024
            sequence = sequence + 1
                
        end_part = original_graph[start:]
        end_part = end.to_bytes(1, byteorder='big') + sequence.to_bytes(1, byteorder='big') + end_part
        end_part = end_part + random_number.to_bytes(2, byteorder='big')
        myAWSIoTMQTTClient.publish(topic, bytearray(end_part), 1)
        print("Published end half of message " + str(loopCount))
        
        loopCount += 1
    time.sleep(float(interval))

print("Finished Publishing")

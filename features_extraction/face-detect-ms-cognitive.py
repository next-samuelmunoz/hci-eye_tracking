#!/usr/bin/env python

########### Python 2.7 #############
import httplib, urllib, base64
import requests
import json
import ConfigParser
import os
from time import sleep


config = ConfigParser.RawConfigParser()
config.read('config.cfg')


INPUT_PATH = config.get('general', 'INPUT_PATH')
OUTPUT_PATH = config.get('general', 'OUTPUT_PATH')
IMAGE_FILENAME = config.get('general', 'IMAGE_FILENAME')
IMAGE_URL = config.get('general', 'IMAGE_URL')
IS_BINARY = config.getboolean('general', 'IS_BINARY')
API_KEY = config.get('credentials', 'COGNITIVE_API_KEY')


# Detect face for data corresponding to a given file
def detect_face(data, IS_BINARY):
    myjson = "{'result': 'FAIL'}"
    content_type = 'application/octet-stream'
    if (not IS_BINARY):
        print "Is not binary"
        payload = {
            'url':IMAGE_URL
        }
        data = json.dumps(payload)
        content_type = 'application/json'

    headers = {
        # Request headers
        'Content-Type': content_type,
        'Ocp-Apim-Subscription-Key': API_KEY
    }

    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'false',
        'returnFaceLandmarks': 'true'
        })

    try:
        protocol = 'https://'
        servername =  'westus.api.cognitive.microsoft.com'
        method = '/face/v1.0/detect?%s' %params
        url = protocol+servername+method

        response = requests.post(url, data=data, headers= headers)

        if response.status_code is not 200:
            # Check rate limits
            if response.status_code == 429:
                sleep(60)
            raise Exception(response.status)

        myjson = response.json()
    except Exception as e:
        print e
    return myjson


# Loop for detecting faces for all files
def detect_faces(input_dir, output_dir, max_images=5000):
    count = 0
    for my_sub_dir in os.listdir(input_dir):
        my_input_dir = input_dir + my_sub_dir
        print my_input_dir
        for filename in os.listdir(my_input_dir):
            with open(os.path.join(my_input_dir, filename), "rb") as f_in:
                data = f_in.read()
            myjson = detect_face(data, IS_BINARY)

            dest_dir = output_dir + my_sub_dir
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            with open(os.path.join(dest_dir, filename.replace("jpg", "json")), "w+") as f_out:
                json.dump(myjson, f_out)
            count=count+1
            if count >= max_images:
                return

print "INPUT_PATH is %s" %INPUT_PATH
print "OUTPUT_PATH is %s" %OUTPUT_PATH
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

detect_faces(INPUT_PATH, OUTPUT_PATH)


####################################

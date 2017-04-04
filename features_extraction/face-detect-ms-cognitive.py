#!/usr/bin/env python

########### Python 2.7 #############
import httplib, urllib, base64
import requests
import json

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')


IMAGE_FILENAME = config.get('general', 'IMAGE_FILENAME')
IMAGE_URL = config.get('general', 'IMAGE_URL')
IS_BINARY = config.getboolean('general', 'IS_BINARY')
API_KEY = config.get('credentials', 'COGNITIVE_API_KEY')

content_type = 'application/octet-stream'
if (IS_BINARY):
    data = open(IMAGE_FILENAME, 'rb').read()
else:
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
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'true'
})

try:
    protocol = 'https://'
    servername =  'westus.api.cognitive.microsoft.com'
    method = '/face/v1.0/detect?%s' %params
    url = protocol+servername+method
    print url

    response = requests.post(url, data=data, headers= headers)

    print response
    print response.json()
except Exception as e:
    print e

####################################

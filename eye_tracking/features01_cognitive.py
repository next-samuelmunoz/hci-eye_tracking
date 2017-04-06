# -*- coding: utf-8 -*-
"""Create first version of the dataset using MS-Cognitive extracted features.

See: https://www.microsoft.com/cognitive-services/en-us/face-api/documentation/face-api-how-to-topics/HowtoDetectFacesinImage#-step-3-understanding-and-using-face-landmarks
"""

import csv
import json
import os
import re
import sys

import config
from utils import Data



if __name__=="__main__":
    # Create destination path
    if os.path.exists(config.PATH_DATA_FEATURES01_COGNITIVE):
        print("Folder {} exists, no need to generate dataset.".format(config.PATH_DATA_FEATURES01_COGNITIVE))
        exit()
    os.makedirs(config.PATH_DATA_FEATURES01_COGNITIVE)
    # Load raw dataset
    data_raw = Data(config.PATH_DATA_RAW)
    data_cognitive = []
    # Cognitive JSON files follows raw dataset structure.
    regexp = re.compile(r'.*/.*/(.*/.*)\.jpg')
    for datum_raw in data_raw.iterate():
        json_cognitive_path = "{}{}.fix.json".format(
            config.PATH_DATA_COGNITIVE,
            regexp.search(datum_raw['img_path']).group(1)
        )
        if os.path.exists(json_cognitive_path):
            with open(json_cognitive_path, 'r') as fd:
                datum_cognitive = json.load(fd)
            try:
                marks = datum_cognitive['faceLandmarks']
                data_cognitive.append(
                    {
                        'img': datum_raw['img_path'],
                        'face_x': datum_cognitive['faceRectangle']['left'],
                        'face_y': datum_cognitive['faceRectangle']['top'],
                        'face_width': datum_cognitive['faceRectangle']['width'],
                        'face_height': datum_cognitive['faceRectangle']['height'],
                        'eye_left_x': marks['eyeLeftOuter']['x'],
                        'eye_left_y': marks['eyeLeftTop']['y'],
                        'eye_left_width': marks['eyeLeftInner']['x']-marks['eyeLeftOuter']['x'],
                        'eye_left_height':  marks['eyeLeftBottom']['y']- marks['eyeLeftTop']['y'],
                        # 'eye_left_image': TODO,
    					'eye_right_x': marks['eyeRightInner']['x'],
    					'eye_right_y': marks['eyeRightTop']['y'],
    					'eye_right_width': marks['eyeRightOuter']['x']-marks['eyeRightInner']['x'],
    					'eye_right_height':  marks['eyeRightBottom']['y']- marks['eyeRightTop']['y'],
                        # 'eye_right_image': TODO,
                        'target_x': datum_raw['x'],
                        'target_y': datum_raw['y'],
                    }
                )
            except Exception as e:
                print "{} \n file: {}".format(e.message, json_cognitive_path)
                print datum_cognitive
        else:
            print "[WARNING] '{}'' NOT FOUND".format(json_cognitive_path)
    # Save dataset
    with open(config.PATH_FEATURES01_COGNITIVE_CSV,'wb') as fd:
        csv_writer = csv.DictWriter(fd, fieldnames=data_cognitive[0].keys())
        csv_writer.writeheader()
        for row in data_cognitive:
            csv_writer.writerow(row)

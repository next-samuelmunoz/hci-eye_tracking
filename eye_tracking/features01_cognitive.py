# -*- coding: utf-8 -*-
"""Create first version of the dataset using MS-Cognitive extracted features.

See: https://www.microsoft.com/cognitive-services/en-us/face-api/documentation/face-api-how-to-topics/HowtoDetectFacesinImage#-step-3-understanding-and-using-face-landmarks
"""

import csv
import hashlib
import json
import os
import sys

import config
from utils import Data

# Bounding boxes by default might be too small.
# This parameter scales the bounding box.
EYE_BBOX_SCALE_WIDTH = 1.2
EYE_BBOX_SCALE_HEIGHT = 1.5


from PIL import Image, ImageOps
def extract_eye(img_path, (bbox_x, bbox_y, bbox_w, bbox_h), (size_x, size_y), dest_path):
    try:
        im = Image.open(img_path).crop((bbox_x, bbox_y, bbox_x+bbox_w, bbox_y+bbox_h)).convert('L')
        ImageOps.autocontrast(im, cutoff=0, ignore=None).resize((size_x, size_y)).save(dest_path)
    except Exception as e:
        print e.message



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
    for datum_raw in data_raw.iterate():
        img_path = datum_raw['img_path'][len(config.PATH_DATA_RAW):]
        json_cognitive_path = "{}{}.fix.json".format(
            config.PATH_DATA_COGNITIVE,
            img_path[:-4]
        )
        if os.path.exists(json_cognitive_path):
            with open(json_cognitive_path, 'r') as fd:
                datum_cognitive = json.load(fd)
            try:
                marks = datum_cognitive['faceLandmarks']
                datum_new = {
                    'face_x': datum_cognitive['faceRectangle']['left'],
                    'face_y': datum_cognitive['faceRectangle']['top'],
                    'face_width': datum_cognitive['faceRectangle']['width'],
                    'face_height': datum_cognitive['faceRectangle']['height'],
                    'eye_left_x': marks['eyeLeftOuter']['x'],
                    'eye_left_y': marks['eyeLeftTop']['y'],
                    'eye_left_width': marks['eyeLeftInner']['x']-marks['eyeLeftOuter']['x'],
                    'eye_left_height':  marks['eyeLeftBottom']['y']- marks['eyeLeftTop']['y'],
                    # 'eye_left_image': None,
                    'eye_right_x': marks['eyeRightInner']['x'],
                    'eye_right_y': marks['eyeRightTop']['y'],
                    'eye_right_width': marks['eyeRightOuter']['x']-marks['eyeRightInner']['x'],
                    'eye_right_height':  marks['eyeRightBottom']['y']- marks['eyeRightTop']['y'],
                    # 'eye_right_image': None,
                }
                # Scale eye bounding boxes
                for eye in ('eye_left','eye_right'):
                    w_pad = datum_new[eye+'_width']*EYE_BBOX_SCALE_WIDTH
                    datum_new[eye+'_x'] -= w_pad//2
                    datum_new[eye+'_width'] += w_pad
                    h_pad = datum_new[eye+'_height']*EYE_BBOX_SCALE_HEIGHT
                    datum_new[eye+'_y'] -= h_pad//2
                    datum_new[eye+'_height'] += h_pad
                data_cognitive.append(datum_new)
                #Type conversion, floats->int pixels
                for k,v in datum_new.iteritems():
                    if type(v)==float:
                        datum_new[k] = int(round(v))
                # Generate eyes imgs
                eye_path = hashlib.md5(datum_raw['img_path']).hexdigest()
                for eye in ('eye_left','eye_right'):
                    datum_new[eye+'_image'] = eye_path+'_'+eye+'.jpg'
                    extract_eye(
                        datum_raw['img_path'],
                        (datum_new[eye+'_x'], datum_new[eye+'_y'],datum_new[eye+'_width'] ,datum_new[eye+'_height']),
                        config.FEATURES01_EYES_SIZE,
                        config.PATH_DATA_FEATURES01_COGNITIVE+datum_new[eye+'_image']
                    )
                # Enrich datum with raw attrs
                datum_raw.pop('img_path')
                datum_new.update(datum_raw)
            except Exception as e:
                print "{} \n file: {}".format(e.message, json_cognitive_path)
                print datum_cognitive
                print datum_new
        else:
            print "[WARNING] '{}' NOT FOUND".format(json_cognitive_path)
    # Save dataset
    with open(config.PATH_FEATURES01_COGNITIVE_CSV,'wb') as fd:
        csv_writer = csv.DictWriter(fd, fieldnames=data_cognitive[0].keys())
        csv_writer.writeheader()
        for row in data_cognitive:
            csv_writer.writerow(row)

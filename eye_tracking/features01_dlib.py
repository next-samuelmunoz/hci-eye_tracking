# -*- coding: utf-8 -*-
"""Create first version of the dataset using MS-Cognitive extracted features.

See: https://www.microsoft.com/cognitive-services/en-us/face-api/documentation/face-api-how-to-topics/HowtoDetectFacesinImage#-step-3-understanding-and-using-face-landmarks
"""

import csv
import hashlib
import json
import os
import sys


import csv
import os
import skimage
import skimage.transform


import config
from utils import Data
from features_dlib import FeaturesDlib


# Bounding boxes by default might be too small.
# This parameter scales the bounding box.
EYE_BBOX_SCALE_WIDTH = 0.9
EYE_BBOX_SCALE_HEIGHT = 1.7


def extract_eye(img, (bbox_x, bbox_y, bbox_w, bbox_h), (size_x, size_y), dest_path):
    try:
        img_eye = img[bbox_x:bbox_y, bbox_x+bbox_w:bbox_y+bbox_h]
        img_eye = skimage.color.rgb2gray(img_eye)
        img_eye = skimage.exposure.equalize_hist(img_eye)
        img_eye = skimage.transform.resize(img_eye,(size_x, size_y))
        skimage.io.imsave(dest_path, img_eye)
    except Exception as e:
        print locals()
        print e.message


def dlib2features01(features):
    retval = {
        'face_x': features['face.x'],
        'face_y': features['face.y'],
        'face_width': features['face.width'],
        'face_height': features['face.height'],
    }
    for eye,points in (
        ('eye_left',(36,37,38,39,40,41)),
        ('eye_right',(42,43,44,45,46,47))
    ):
        eye_points = [
            (features[str(p)+'.x'], features[str(p)+'.y'])
            for p in points
        ]
        x = min([i for i,_ in eye_points])
        y = min([i for _,i in eye_points])
        w = max([i for i,_ in eye_points])-x
        h = max([i for _,i in eye_points])-y
        # Scale eye bounding boxes
        w_pad = w*EYE_BBOX_SCALE_WIDTH
        retval[eye+'_x'] = int(x-w_pad//2)
        retval[eye+'_width'] = int(w+w_pad)
        h_pad = h*EYE_BBOX_SCALE_HEIGHT
        retval[eye+'_y'] = int(y-h_pad//2)
        retval[eye+'_height'] = int(h+h_pad)
    return retval



if __name__=="__main__":
    # Create destination path
    if os.path.exists(config.PATH_DATA_FEATURES01_DLIB):
        print("Folder {} exists, no need to generate dataset.".format(config.PATH_DATA_FEATURES01_DLIB))
        exit()
    os.makedirs(config.PATH_DATA_FEATURES01_DLIB)
    features = FeaturesDlib(config.PATH_DLIB_MODEL)
    data = Data(config.PATH_DATA_RAW)
    i = 0
    with open(config.PATH_FEATURES01_DLIB_CSV,'wb') as fd:
        for datum in data.iterate():
            img_path = datum['img_path']
            img = skimage.io.imread(img_path)
            # TODO: data augmentation in memory, nest in a loop
            f = features.extract_features(img)
            if f == -1:  # No face
                print "[WARNING] '{}' FACE NOT FOUND".format(img_path)
            elif f == -2:  # No landmarks
                print "[WARNING] '{}' LANDMARKS NOT FOUND".format(img_path)
            else:  # Everything correct
                f = dlib2features01(f)
                f.update(datum)
                f['img'] = '/'.join(img_path.split('/')[-2:])
                # TODO: Generate eyes
                eye_path = hashlib.md5(img_path).hexdigest()
                for eye in ('eye_left','eye_right'):
                    f[eye+'_image'] = eye_path+'_'+eye+'.jpg'
                    # extract_eye(
                    #     img,
                    #     (f[eye+'_x'], f[eye+'_y'],f[eye+'_width'] ,f[eye+'_height']),
                    #     config.FEATURES01_EYES_SIZE,
                    #     config.PATH_DATA_FEATURES01_DLIB+f[eye+'_image']
                    # )
                if i==0:
                    csv_writer = csv.DictWriter(fd, fieldnames=f.keys())
                    csv_writer.writeheader()
                if f:
                    csv_writer.writerow(f)
                i+=1
                print i

# -*- coding: utf-8 -*-
"""Create first version of the dataset.

Required deb packages: opencv-data

http://docs.opencv.org/trunk/d7/d8b/tutorial_py_face_detection.html
"""

"""
Warning
Status is experimental, just for testing
"""

import numpy as np
import cv2

# img_path = "/home/samuelmunoz/beeva/github/hci-eye_tracking/eye_tracking/data/raw/ee14fdd4-eb9c-4b7f-a8df-db5ea06faff6_1366_768_14_TC_glasses-no/1489664910_441_106_8.jpg"


class Features01(object):

    def __init__(self,
        face_classifier_path='/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml',
        eyes_classifier_path='/usr/share/opencv/haarcascades/haarcascade_eye.xml'
    ):
        self.face_cascade = cv2.CascadeClassifier(face_classifier_path)
        self.eye_cascade = cv2.CascadeClassifier(eyes_classifier_path)
        self.face_scale = 1.01
        self.face_min_size = (100,200)
        self.eye_scale = 1.01
        self.eye_min_size = (30,20)


    def extract_features(self, img_path):
        retval = None
        gray = cv2.equalizeHist(cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2GRAY))
        # Detect face
        faces = self.face_cascade.detectMultiScale(gray, self.face_scale, 5, 0, self.face_min_size)
        if faces!=():
            biggest_face = max(faces, key=lambda (x,y,w,h): w*h)
            face_x, face_y, face_w, face_h = biggest_face
            # Detect eyes
            roi_gray = cv2.equalizeHist(gray[face_y:face_y+face_h, face_x:face_x+face_w])
            eyes = self.eye_cascade.detectMultiScale(roi_gray, self.eye_scale, 5, 0, self.eye_min_size)
            if len(eyes) == 2:
                eye_left, eye_right = eyes
                if eyes[0][0]>eyes[0][1]:
                    eye_left, eye_right = eyes[1], eyes[0]
                retval = {
                    'face_x': face_x,
                    'face_y': face_y,
                    'face_width': face_w,
                    'face_height': face_h,
                    'eye_left_x': eye_left[0],
                    'eye_left_y': eye_left[1],
                    'eye_left_width': eye_left[2],
                    'eye_left_height':  eye_left[3],
                    # 'eye_left_image': None,
                    'eye_right_x': eye_right[0],
                    'eye_right_y': eye_right[1],
                    'eye_right_width': eye_right[2],
                    'eye_right_height':  eye_right[3],
                    # 'eye_right_image': None,
                }
            else:
                print "[WARNING] '{}' 2 EYES NOT FOUND".format(img_path)
        else:
            print "[WARNING] '{}' FACE NOT FOUND".format(img_path)
        return retval



if __name__=="__main__":
    import config
    from utils import Data

    features = Features01()
    data = Data(config.PATH_DATA_RAW)
    count = 0
    i = 0
    for datum in data.iterate():
        # print datum

        # print features.extract_features(datum['img_path'])
        if features.extract_features(datum['img_path']):
            count += 1
        i +=1
    print i, count

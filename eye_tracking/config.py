# -*- coding: utf-8 -*-


#
### PATHS DATASETS
#
PATH_DATA = 'data/'
PATH_DATA_RAW = PATH_DATA+'raw/'

# cognitive
PATH_DATA_COGNITIVE = PATH_DATA+'cognitive/'
PATH_DATA_FEATURES01_COGNITIVE = PATH_DATA+'features01_cognitive/'
PATH_FEATURES01_COGNITIVE_CSV = PATH_DATA_FEATURES01_COGNITIVE+'features.csv'

# dlib
PATH_DLIB_MODEL = PATH_DATA+'shape_predictor_68_face_landmarks.dat'
PATH_DATA_DLIB = PATH_DATA+'dlib/'
PATH_DATA_DLIB_CSV = PATH_DATA_DLIB+'features.csv'
PATH_DATA_FEATURES01_DLIB = PATH_DATA+'features01_dlib/'
PATH_FEATURES01_DLIB_CSV = PATH_DATA_FEATURES01_DLIB+'features.csv'

#
### DATASET CONSTANTS
#
FEATURES01_EYES_SIZE = (30,20)


#
### GAME / CALIBRATION
#

# SCREEN
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_DIAGONAL =  14  # Not used

# WEBCAM
CAM_DEVICE = "/dev/video0"
CAM_WIDTH = 1280
CAM_HEIGHT = 720
"""
-NOT USED-
Position of the camera respect to the screen.
Format is XX where X can be:
T: top
B: bottom
C: center
L: left
R: right
"""
CAM_POSITION = "TC"


# IMAGES
IMG_BACKGROUND = 'img/bg-sky.jpg'
IMG_TARGET = 'img/target01.png'


# OTHER
TIME_GAME = 60  # Seconds
FAILS = 5  # Hits a user can fail
RADIUS = 75.0  # Radius of the target, centered in the image


try:
    from config_local import *
except:
    pass

# -*- coding: utf-8 -*-


#
### PATHS
#
PATH_DATA = 'data/'
PATH_DATA_RAW = PATH_DATA+'raw/'


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

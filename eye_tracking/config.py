# -*- coding: utf-8 -*-


#
### Screen
#
SCREEN_WIDTH = 1680
SCREEN_HEIGHT = 1050
SCREEN_DIAGONAL =  14  # Not used


#
### Webcam
#
CAM_DEVICE = "/dev/video0"
CAM_WIDTH = 1280
CAM_HEIGHT = 720
CAM_POSITION = "TOP-CENTERED"  # Not used


#
### Images
#
IMG_BACKGROUND = 'img/bg-sky.jpg'
IMG_TARGET = 'img/target01.png'


#
### Game
#
FAILS = 5
RADIUS = 75.0

#
### Paths
#
PATH_RAW = 'data/raw'


try:
    from config_local import *
except:
    pass

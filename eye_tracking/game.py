# -*- coding: utf-8 -*-
"""Game to generate a dataset
"""


import time

import pygame

import config
from utils import Data, Webcam
import utils.game



#
### Initialize
#
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(
    (config.SCREEN_WIDTH, config.SCREEN_HEIGHT),
    #pygame.locals.FULLSCREEN|pygame.locals.DOUBLEBUF
)



#
### Stages
#
# Intro
stage_intro = utils.game.StageIntro(screen, config)
user_wears_glasses = stage_intro.loop()
# Webcam
webcam = Webcam(config.CAM_DEVICE, config.CAM_WIDTH, config.CAM_HEIGHT)
time.sleep(1)  # wait util webcam is initialized
stage_webcam = utils.game.StageWebcam(screen, webcam, config)
stage_webcam.loop()
# Game
data = Data(
    raw_data_path=config.PATH_DATA_RAW,
    screen_width=config.SCREEN_WIDTH,
    screen_height=config.SCREEN_HEIGHT,
    screen_diagonal=config.SCREEN_DIAGONAL,
    camera_position=config.CAM_POSITION,
    glasses = user_wears_glasses
)
data.new_game()
stage_game = utils.game.StageGame(screen, webcam, data, config)
scores = stage_game.loop()
webcam.close()


#
### Terminate
#
pygame.font.quit()
pygame.display.quit()

print "HITS: {}".format(len(scores))
print "PRECISSION: {}".format(sum(scores)/float(len(scores)))
# print "REMAINING TIME: -".format()
print "TOTAL SCORE: {}".format(sum(scores))

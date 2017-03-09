# -*- coding: utf-8 -*-

import random

import pygame
from pygame.locals import *

import config
from utils import Data, Webcam


class Screen(object):
    def __init__(self, width, height):
        self.screen = None
        self.background = pygame.image.load(config.IMG_BACKGROUND)
        self.target = pygame.image.load(config.IMG_TARGET)
        self.screen = pygame.display.set_mode(
            (width, height),
            FULLSCREEN|DOUBLEBUF
        )

    def print_target(self, x, y, size_x, size_y):
        """Print the background and a target.
        x, y: int
            Position of the center of the target.
        x_size, y_size: int
            Size of the target.
        """
        self.screen.blit(self.background, (0,0))  # Background
        # Target
        new_target = pygame.transform.scale(self.target, (size_x, size_y))
        self.screen.blit(new_target, (x-(size_x/2),y-(size_y/2)) )
        pygame.display.update()


# Global params
data = Data(
    raw_data_path=config.PATH_DATA_RAW,
    screen_width=config.SCREEN_WIDTH,
    screen_height=config.SCREEN_HEIGHT,
    screen_diagonal=config.SCREEN_DIAGONAL,
    camera_position=config.CAM_POSITION
)
webcam = Webcam(config.CAM_DEVICE, resolution=(config.CAM_WIDTH, config.CAM_HEIGHT))
pygame.init()
screen = Screen(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)



# New game
data.new_game()
fails = config.FAILS
scores = []
exit = False
while not exit:
    click = False
    x=random.randint(0, config.SCREEN_WIDTH)
    y=random.randint(0, config.SCREEN_HEIGHT)
    screen.print_target(x, y, 150, 150)
    while not click and not exit:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    exit = True
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                distance = (((x-mouse_x)**2+(y-mouse_y)**2)**0.5)/config.RADIUS
                if distance<=1:  # Target is hit, take picture!
                    webcam.capture(data.create_datum(mouse_x, mouse_y))
                    scores.append(int(((1-distance)*6)+5))
                    click = True
                else:
                    fails -= 1
                    if fails == 0:
                        exit = True


#
### Terminate game
#
webcam.close()
print "HITS: {}".format(len(scores))
print "PRECISSION: {}".format(sum(scores)/float(len(scores)))
# print "REMAINING TIME: -".format()
print "TOTAL SCORE: {}".format(sum(scores))

# -*- coding: utf-8 -*-
"""Tool to inspect the raw dataset.
"""


import pygame
from pygame.locals import *

import config
from utils import Data


def loop(screen, data_list):
    i_data = 0
    exit = 0
    while not exit:
        screen.blit(
            pygame.transform.scale(
                pygame.transform.flip(
                    pygame.image.load(data_list[i_data]['img_path']),
                    True, False
                ),
                (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
            ),
            (0,0)
        )
        pygame.draw.circle(screen, (255,0,0), (data_list[i_data]['x'],data_list[i_data]['y']), 25, 0)
        pygame.display.update()
        click = False
        while not click:
            for event in pygame.event.get():
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        exit = True
                        click = True
                    elif event.key == K_RIGHT:
                        if i_data<len(data_list)-1:
                            i_data += 1
                            click = True
                    elif event.key == K_LEFT:
                        if i_data>0:
                            i_data -= 1
                            click = True



data = Data(config.PATH_DATA_RAW)
data_list = list(data.iterate())
if data_list:
    print "NUMBER OF SAMPLES: {}".format(len(data_list))
    pygame.init()
    screen = pygame.display.set_mode(
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT),
        # pygame.locals.FULLSCREEN|pygame.locals.DOUBLEBUF
    )
    loop(screen, data_list)
    pygame.display.quit()
else:
    print "No data"

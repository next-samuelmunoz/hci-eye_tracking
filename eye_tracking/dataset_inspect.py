# -*- coding: utf-8 -*-
"""Tool to inspect the raw dataset.
"""

import csv

import pygame
from pygame.locals import *

import config
from utils import Data

def get_img_id(game_id, timestamp):
    return '{}_{}'.format(game_id, timestamp)

DATASETS_01 = {
    False: None,
    config.PATH_FEATURES01_COGNITIVE_CSV: None,
    config.PATH_FEATURES01_DLIB_CSV: None
}


def loop(data_list):
    pygame.init()
    i_data = 0
    exit = 0
    flag_dot = False
    ds01_key_index = 0
    # Calculate webcam image position
    img = pygame.image.load(data_list[i_data]['img_path'])
    img_w, img_h = img.get_rect().size
    if data_list[i_data]['camera_position'] == 'TC':
        img_pos = ((data_list[i_data]['screen_width']-img_w)/2,0)
    else:
        img_pos = (0,0)

    screen = pygame.display.set_mode(
        (data_list[i_data]['screen_width'],data_list[i_data]['screen_height'])
    )
    while not exit:
        img = pygame.image.load(data_list[i_data]['img_path'])
        print(data_list[i_data])
        #Print user screen limits
        ds01_key = DATASETS_01.keys()[ds01_key_index]
        print ds01_key
        if ds01_key:  # Show detected features
            try:
                if DATASETS_01[ds01_key]==None: # Load dataset
                    DATASETS_01[ds01_key] = {}
                    with open(ds01_key,'rb') as fd:
                        csv_reader = csv.DictReader(fd)
                        for row in csv_reader:
                            DATASETS_01[ds01_key][get_img_id(row['game_id'],row['timestamp'])] = row
                features = DATASETS_01[ds01_key][get_img_id(data_list[i_data]['game_id'],data_list[i_data]['timestamp'])]
                pygame.draw.rect( # Face
                    img, (0,0,255),
                    [int(features[x]) for x in ('face_x','face_y','face_width','face_height')],
                    3
                )
                pygame.draw.rect( # Left eye
                    img, (0,255,0),
                    [int(float(features[x])) for x in ('eye_left_x','eye_left_y','eye_left_width','eye_left_height')],
                    1
                )
                pygame.draw.rect(  # Right Eye
                    img, (0,255,0),
                    [int(float(features[x])) for x in ('eye_right_x','eye_right_y','eye_right_width','eye_right_height')],
                    1
                )
                print features
            except Exception as e:
                print "Dataset {} failed: {}".format(ds01_key, e.message)
        screen.fill((0,0,0))
        screen.blit(img, img_pos)
        if flag_dot:  # Show dot
            pygame.draw.circle(screen, (255,0,0), (-data_list[i_data]['x']+data_list[i_data]['screen_width'],data_list[i_data]['y']), 25, 0)
        pygame.display.update()
        click = False
        while not click:
            # for event in pygame.event.get():
            event = pygame.event.wait()
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
                elif event.key == K_d: # Switch dot (where the user looks)
                    flag_dot = False if flag_dot else True
                    click = True
                elif event.key == K_1: # Switch DS01 mscognitive, dlib
                    ds01_key_index = (ds01_key_index+1) % len(DATASETS_01)
                    print ds01_key_index
                    click = True
            pygame.event.clear()
    pygame.display.quit()



data = Data(config.PATH_DATA_RAW)
data_list = list(data.iterate())
if data_list:
    print "NUMBER OF SAMPLES: {}".format(len(data_list))
    loop(data_list)
else:
    print "No data"

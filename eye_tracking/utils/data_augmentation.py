# -*- coding: utf-8 -*-
"""Perform data augmentation on images
"""

import pygame
from pygame.locals import *
from data import Data
import skimage
from skimage import io
from skimage import transform
import numpy as np
import os

PATH_DATA = '../data/'
PATH_DATA_RAW = '../data/raw/'
PATH_DATA_AUGMENTED = '../data/augmented/'

def data_augmentation(img, transformations=[]):
    """Iterate over transformations and return the transformed image.


    Parameters
    ----------
    img:
        Opened image with skimage.io.imread()
    transformations: function(img)
        Function to augment the image.

    Returns
    -------
    img: generator of transformed images.
    """
    if transformations == []:
        yield img
    else:
        for img_candidate in transformations[0](img):
            for x in data_augmentation(img_candidate, transformations[1:]):
                yield x

#
### Transformations
#

def mirror(img):
    """Vertical symmetry
    """
    img = np.fliplr(img)
    return img


def noise(img):
    """Add some noise
    """
    yield img
    pass


def luminance(img):
    """Change ilumination
    """
    yield img
    pass


def loop(data_list):
    for i_data in range(len(data_list)):
        img = io.imread(data_list[i_data]['img_path'])
        #print(data_list[i_data])

        mypath = data_list[i_data]['img_path'].replace(PATH_DATA_RAW, PATH_DATA_AUGMENTED)
        dest_dir = os.path.dirname(mypath)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        img = mirror(img)
        io.imsave(mypath, img)


data = Data(PATH_DATA_RAW)
data_list = list(data.iterate())
if data_list:
    print "NUMBER OF SAMPLES: {}".format(len(data_list))
    loop(data_list)
else:
    print "No data"

# -*- coding: utf-8 -*-
"""Perform data augmentation on images
"""

import pygame
from pygame.locals import *
from data import Data
import skimage
from skimage import io
import numpy as np
import os
from skimage.restoration import denoise_bilateral
from skimage.util import random_noise
from skimage.exposure import equalize_hist

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
    yield img
    img = np.fliplr(img)
    yield img


def bilateral(img):
    """Apply bilateral filter
    """
    yield img
    img = denoise_bilateral(img, sigma_spatial=2, multichannel=True)
    yield img

def noise(img):
    """Add gaussian noise
    """
    yield img
    img = random_noise(img, mode='gaussian', var=0.01)
    yield img

def equalize(img):
    """Equalize histogram
    """
    yield img
    img = equalize_hist(img, nbins=256, mask=None)
    yield img


def loop(data_list):
    for i_data in range(len(data_list)):
        img = io.imread(data_list[i_data]['img_path'])

        mypath = data_list[i_data]['img_path'].replace(PATH_DATA_RAW, PATH_DATA_AUGMENTED)
        dest_dir = os.path.dirname(mypath)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        i = 0
        for img_i in data_augmentation(img, [mirror, noise, bilateral, equalize]):
            io.imsave(mypath.replace(".jpg", "_{}.jpg".format(str(i))), img_i)
            i+=1


if __name__ == "__main__":

    data = Data(PATH_DATA_RAW)
    data_list = list(data.iterate())
    if data_list:
        print "NUMBER OF SAMPLES: {}".format(len(data_list))
        loop(data_list)
    else:
        print "No data"

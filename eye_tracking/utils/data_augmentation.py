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
# These functions are generators.
# First yield image without transformation
# Yield transformed images

def mirror(img):
    """Vertical symmetry
    """
    yield img
    yield np.fliplr(img)


def bilateral(img):
    """Apply bilateral filter
    """
    yield img
    yield skimage.util.img_as_ubyte(
        denoise_bilateral(img, sigma_spatial=2, multichannel=True),
        force_copy=False
    )

def noise(img):
    """Add gaussian noise
    """
    yield img
    yield skimage.util.img_as_ubyte(
        random_noise(img, mode='gaussian', var=0.01),
        force_copy=False
    )

def equalize(img):
    """Equalize histogram
    """
    yield img
    yield skimage.util.img_as_ubyte(
        equalize_hist(img, nbins=256, mask=None),
        force_copy=False
    )

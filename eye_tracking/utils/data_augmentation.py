# -*- coding: utf-8 -*-
"""Perform data augmentation on images
"""


def data_augmentation(img, transformations=[]):
    """Iterate over transformations and return the transformed image.


    Parameters
    ----------
    img:
        Opened image
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
    pass


def noise(img):
    """Add some noise
    """
    yield img
    pass

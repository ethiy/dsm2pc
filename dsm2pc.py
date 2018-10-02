#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from geo2d import GeoRaster

import numpy as np


def is_heightmap(image_array):
    w, h, *_ = image_array.shape
    return image_array.size == w * h and image_array.dtype == np.float


def heightmap_to_pointcloud(image_array, origin, pixel_size):
    if not is_heightmap(image_array):
        raise TypeError("The input image array does not represent a height map!")
    else:
        return [
            (
                origin[0] + pixel_size[0] * i,
                origin[1] + pixel_size[1] * j,
                height
            )
            for (i, j), height in np.ndenumerate(image_array)
        ]
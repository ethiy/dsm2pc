#! /usr/bin/env python3
# -*- coding: <utf-8> -*-

"""dsm2las.

Usage:
    dsm2las (-h | --help)
    dsm2las --version
    dsm2las <dsm_file> <las_file> [--scale=<sc>]

Options:
    -h --help           Show this screen.
    --scale=<sc>        Scale [default: 1].
    --version           Show version.

"""

__version__ = '0.1.0a1'


import docopt

from geo2d import GeoRaster

import numpy as np
from skimage.transform import rescale

from laspy.file import File
from laspy.header import Header


def is_heightmap(image_array):
    w, h, *_ = image_array.shape
    return image_array.size == w * h and image_array.dtype == np.float


def heightmap_to_pointcloud(image_array, origin, pixel_size, scale=1):
    if not is_heightmap(image_array):
        raise TypeError("The input image array does not represent a height map!")
    else:
        return [
            (
                origin[0] + pixel_size[0] * j,
                origin[1] + pixel_size[1] * i,
                height
            )
            for (i, j, *_), height in np.ndenumerate(
                rescale(image_array, scale)
            )
        ]


def georaster_to_pointcloud(georaster, scale=1):
    return heightmap_to_pointcloud(
        georaster.image,
        georaster.reference_point,
        georaster.pixel_sizes,
        scale
    )


def dsm_to_pointcloud(dsm_file, scale=1):
    return georaster_to_pointcloud(
        GeoRaster.GeoRaster.from_file(dsm_file),
        scale
    )


def dsm_to_las(dsm_file, las_file, scale=1):
    with File(las_file, mode='w', header=Header()) as las:
        las.X, las.Y, las.Z = zip(
            * dsm_to_pointcloud(dsm_file, scale)
        )


def main():
    arguments = docopt.docopt(
        __doc__,
        help=True,
        version=__version__,
        options_first=False
    )
    dsm_to_las(
        arguments['<dsm_file>'],
        arguments['<las_file>'],
        float(arguments['--scale'])
    )
    

if __name__ == '__main__':
    main()
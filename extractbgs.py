#!/usr/bin/env python
#
# Copyright (c) 2016 Matthew Earl
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#     The above copyright notice and this permission notice shall be included
#     in all copies or substantial portions of the Software.
# 
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#     OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#     MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
#     NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#     DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#     OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
#     USE OR OTHER DEALINGS IN THE SOFTWARE.



"""
Extract background images from a tar archive.

"""


__all__ = (
    'extract_backgrounds',
)


import os
import sys
import tarfile

import cv2
import numpy


def im_from_file(f):
    a = numpy.asarray(bytearray(f.read()), dtype=numpy.uint8)
    return cv2.imdecode(a, cv2.IMREAD_GRAYSCALE)


def extract_backgrounds(archive_name):
    """
    从指定的Tar压缩包中提取JPG格式图片，将图片转换为灰度图，裁剪为方形，并缩放到256x256大小
    转换后的图片保存到./bgs目录
    :param archive_name: 包含有JPG图片的压缩包位置
    """
    os.mkdir("bgs")

    t = tarfile.open(name=archive_name)

    def members():
        m = t.next()
        while m:
            yield m
            m = t.next()
    index = 0
    for m in members():
        if not m.name.endswith(".jpg"):
            continue
        f = t.extractfile(m)
        try:
            im = im_from_file(f)
        finally:
            f.close()
        if im is None:
            continue
        
        if im.shape[0] > im.shape[1]:
            im = im[:im.shape[1], :]
        else:
            im = im[:, :im.shape[0]]
        if im.shape[0] > 256:
            im = cv2.resize(im, (256, 256))
        fname = "bgs/{:08}.jpg".format(index)
        print(fname)
        rc = cv2.imwrite(fname, im)
        if not rc:
            raise Exception("Failed to write file {}".format(fname))
        index += 1


if __name__ == "__main__":

    extract_backgrounds(sys.argv[1])


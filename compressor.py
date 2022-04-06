# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 11:29:28 2022

@author: David Onyeali
"""

from PIL import Image


def read_image(img_path):
    """Read in image and handle error if image is unreadable.
    """
    try:
        img = Image.open(img_path)
    except OSError:
        return "Invalid file type!, valid file types include:\
.jpg, .png, .bmp, .ppm, etc"
    return img



def compress(img, compressed_img_path="compressed.jpg"):
    """Compress image.
    """
    extension = img.format
    if extension == "PNG":
        img.save(compressed_img_path, "JPEG", quality=10)

    elif extension == "JPEG":
        img.save(compressed_img_path, "JPEG", quality=20)
        
    else:
        img.save(compressed_img_path, "JPEG", quality=20)
        
        







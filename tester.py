# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 13:02:04 2022

@author: Babban Gona
"""

import os
from compressor import read_image, compress

os.listdir("images")
           
fname1 = "gear4.jpg"
fname2 = "rengoku.jpg"
fname3 = "yuno.png"


def main(fname):
    
    images_path = "images/"
    
    fpath = images_path + fname
    img = read_image(fpath)
    
    
    compressed_fpath = images_path + "compressed_" + fname
    compress(img, compressed_fpath)
    compressed_img = read_image(compressed_fpath)
    
    
    uncompressed_img_size = round((os.stat(fpath).st_size / 1024 / 1024), 4)
    compressed_img_size = round((os.stat(compressed_fpath).st_size / 1024 / 1024), 4)
    compression_ratio = int(100 - (100 * (compressed_img_size / uncompressed_img_size)))
    print(f"Compression Ratio: {compression_ratio}% - {fname}: {compressed_img.format}")
    
    
for fname in [fname1, fname2, fname3]:\
    main(fname)
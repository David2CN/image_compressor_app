import os
from compressor import read_image, compress, merge

fnames = os.listdir("images")
#uploaded file would be temporarily saved here

print(fnames)
print(os.getcwd())

def do_compression(fname):
    images_path = "images/"
    
    fpath = images_path + fname
    img = read_image(fpath)

    compressed_fpath = images_path + "compressed_" + fname
    compress(img, compressed_fpath)
    compressed_img = read_image(compressed_fpath)
    
    uncompressed_img_size = round((os.stat(fpath).st_size / 1024**2), 4)
    compressed_img_size = round((os.stat(compressed_fpath).st_size / 1024**2), 4)
    compression_ratio = int(100 - (100 * (compressed_img_size / uncompressed_img_size)))
    
    #To display compressed size in kb or mb
    size_unit = "mb"
    if compressed_img_size < 1:
        compressed_img_size *= 1024
        size_unit = "kb"
        
    print(f"Original size: {uncompressed_img_size}mb Compressed size: {compressed_img_size}{size_unit}")
    print(f"Compression Ratio: {compression_ratio}% - {fname}: {compressed_img.format}")
    
    merged_img = merge(img, compressed_img)
    merged_img.show()
    
fname = "gear4.jpg"  #assumption is that the picture is in the images folder
do_compression(fname)


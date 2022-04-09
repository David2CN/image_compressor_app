import os
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
        img.save(compressed_img_path, "PNG", quality=10)

    elif extension == "JPEG":
        img.save(compressed_img_path, "JPEG", quality=10)

    else:
        img.save(compressed_img_path, "JPEG", quality=10)


def merge(im1, im2):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im


def do_compression(fname, do_merge=False):
    images_path = "static/images/"
    fpath = images_path + fname
    img = read_image(fpath)

    compressed_fpath = images_path + "compressed_" + fname
    compress(img, compressed_fpath)
    compressed_img = read_image(compressed_fpath)

    uncompressed_img_size = round((os.stat(fpath).st_size / 1024**2), 4)
    compressed_img_size = round((os.stat(compressed_fpath).st_size / 1024**2), 4)
    compression_ratio = int(100 - (100 * (compressed_img_size / uncompressed_img_size)))


    #To display uncompressed size in kb or mb
    img_size_unit = "mb"
    if uncompressed_img_size < 1:
        uncompressed_img_size *= 1024
        img_size_unit = "kb"

    #To display compressed size in kb or mb
    compressed_size_unit = "mb"
    if compressed_img_size < 1:
        compressed_img_size *= 1024
        compressed_size_unit = "kb"

    print(f"Original size: {uncompressed_img_size}{img_size_unit} Compressed size: {compressed_img_size}{compressed_size_unit}")
    print(f"Compression Ratio: {compression_ratio}% - {fname}: {compressed_img.format}")

    if do_merge:
        merged_img = merge(img, compressed_img)
        merged_img.show()

    return str(uncompressed_img_size)+img_size_unit, str(compressed_img_size)+compressed_size_unit, compression_ratio

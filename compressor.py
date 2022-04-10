import os
from PIL import Image

IMG_PATH = "static/images/"


def read_image(img_path):
    """Read in image and handle error if image is unreadable.
    """
    try:
        img = Image.open(img_path)
    except OSError:
        return "Invalid file type!, valid file types include:\
.jpg, .png, .jpeg, .gif, etc"
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


def get_paths(filename, images_path=IMG_PATH):
    filepath = images_path + filename
    compressed_filepath = images_path + "compressed_" + filename
    return filepath, compressed_filepath


def get_img_size(filepath):
    img_size = round((os.stat(filepath).st_size / 1024**2), 4)  # in MegaBytes
    return img_size


def get_size_units(img_size):
    # To display uncompressed size in kb or mb
    img_size_unit = "mb"
    if img_size < 1:
        img_size *= 1024
        img_size_unit = "kb"
    return img_size_unit


def do_compression(filename):
    filepath, compressed_filepath = get_paths(filename)

    img = read_image(filepath)
    compress(img, compressed_filepath)
    compressed_img = read_image(compressed_filepath)

    uncompressed_img_size = get_img_size(filepath)
    compressed_img_size = get_img_size(compressed_filepath)
    compression_ratio = int(100 - (100 * (compressed_img_size / uncompressed_img_size)))

    # To display uncompressed size in kb or mb
    img_size_unit = get_size_units(uncompressed_img_size)
    compressed_size_unit = get_size_units(compressed_img_size)

    print(f"Original size: {uncompressed_img_size}{img_size_unit} Compressed size: {compressed_img_size}{compressed_size_unit}")
    print(f"Compression Ratio: {compression_ratio}% - {filename}: {compressed_img.format}")

    return str(uncompressed_img_size)+img_size_unit, \
           str(compressed_img_size)+compressed_size_unit, \
           compression_ratio

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


def get_paths(filename, images_path=IMG_PATH):
    filepath = images_path + filename
    compressed_filepath = images_path + "compressed_" + filename
    return filepath, compressed_filepath


def get_size_units(img_size):
    # To get uncompressed size in kb or mb
    img_size_unit = "mb"
    if img_size < 1:
        img_size *= 1024
        img_size_unit = "kb"
    return f"{img_size: .2f}{img_size_unit}"


def get_img_size(filepath):
    img_size = (os.stat(filepath).st_size / 1024**2)  # in MegaBytes
    return round(img_size, 2)


def compress(img, compressed_img_path="compressed.jpg"):
    """Compress image.
    """
    extension = img.format

    if extension == "PNG":
        img.save(compressed_img_path, "PNG", quality=10)

    elif extension == "JPEG":
        img.save(compressed_img_path, "JPEG", quality=50)

    elif extension == "GIF":
        img.save(compressed_img_path, "GIF", quality=50)

    else:
        img.save(compressed_img_path, "JPEG", quality=50)


def do_compression(filename):
    filepath, compressed_filepath = get_paths(filename)

    # read in image, compress and read in compressed image
    img = read_image(filepath)
    compress(img, compressed_filepath)
    compressed_img = read_image(compressed_filepath)

    # get compression ratio
    uncompressed_img_size = get_img_size(filepath)
    compressed_img_size = get_img_size(compressed_filepath)
    compression_ratio = int((1 - (compressed_img_size / uncompressed_img_size)) * 100)

    # get sizes in correct units for display
    img_size_with_unit = get_size_units(uncompressed_img_size)
    compressed_img_size_with_unit = get_size_units(compressed_img_size)

    print(f"Original size: {img_size_with_unit} Compressed size: {compressed_img_size_with_unit}")
    print(f"Compression Ratio: {compression_ratio}% - {filename}: {compressed_img.format}")
    return img_size_with_unit, compressed_img_size_with_unit, compression_ratio


def merge(img1, img2):
    w = img1.size[0] + img2.size[0]
    h = max(img1.size[1], img2.size[1])
    merged_image = Image.new("RGBA", (w, h))
    merged_image.paste(img1)
    merged_image.paste(img2, (img1.size[0], 0))
    return merged_image

import os
import time
from PIL import Image


abspath = os.getcwd()
directory = "imgcomp/static/images/"
IMG_PATH = os.path.join(abspath, directory)


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
    img_size /= 1024  # first convert to KB

    img_size_unit = "kb"
    if img_size >= 1024:   # convert the file to mb if the file is greater than 1024kb (1mb)
        img_size /= 1024
        img_size_unit = "mb"

    return f"{img_size: .2f}{img_size_unit}"


def compress(img, compressed_img_path=directory+"compressed.jpg"):
    """Compress image.
    """
    extension = img.format

    if extension == "PNG":
        img.save(compressed_img_path, "PNG", optimize=True, quality=10)

    elif extension == "JPEG":
        img.save(compressed_img_path, "JPEG", optimize=True, quality=50)

    elif extension == "GIF":
        img.save(compressed_img_path, "GIF", optimize=True, quality=50)

    else:
        img.save(compressed_img_path, "JPEG", optimize=True, quality=50)

    compressed_img = read_image(compressed_img_path)
    return compressed_img


def do_compression(filename):
    filepath, compressed_filepath = get_paths(filename)

    # read in image, compress and read in compressed image
    img = read_image(filepath)
    compressed_img = compress(img, compressed_filepath)

    # get compression ratio in bytes
    uncompressed_img_size = os.path.getsize(filepath)
    compressed_img_size = os.path.getsize(compressed_filepath)
    compression_ratio = int((1 - (compressed_img_size / uncompressed_img_size)) * 100)

    # get sizes in correct units for display
    img_size_with_unit = get_size_units(uncompressed_img_size)
    compressed_img_size_with_unit = get_size_units(compressed_img_size)

    print(f"Original size: {img_size_with_unit} Compressed size: {compressed_img_size_with_unit}")
    print(f"Compression Ratio: {compression_ratio}% - {filename}: {compressed_img.format}")

    return img_size_with_unit, compressed_img_size_with_unit, compression_ratio


def get_resolution(image_filepath):
    img_res = read_image(image_filepath).size
    return f"{img_res[0]}x{img_res[1]}"


def merge(img1, img2):
    w = img1.size[0] + img2.size[0]
    h = max(img1.size[1], img2.size[1])

    merged_image = Image.new("RGBA", (w, h))

    merged_image.paste(img1)
    merged_image.paste(img2, (img1.size[0], 0))

    return merged_image


def clear_images(limit=5):
    """To delete images that have exceeded storage time
    """
    try:
        files = os.listdir(IMG_PATH)
        for file in files:
            if file not in ["logo.ico", "logo.png"]:
                filepath = os.path.join(IMG_PATH, file)

                time_created = os.path.getctime(filepath)
                now = time.time()

                duration = now - time_created
                if duration >= limit*60:
                    # delete file
                    os.remove(filepath)

                    print("Storage cleared!")
    except FileNotFoundError:
        pass
    except:
        pass

import pytest

from compressor import do_compression, read_image, compress, get_size_units

img_path = "static/images/akaza.png"

def test_read_image():
    assert read_image("hello"), "Invalid file type!, valid file types include:\
.jpg, .png, .jpeg, .gif, etc"
    # assert (type(read_image(img_path)), type())

def test_compress():
    img = read_image(img_path)
    assert type(compress(img)), type(img)

def test_get_size_units():
    assert get_size_units(0.1), "kb"
    assert get_size_units(2), "mb"

def test_do_compression():
    assert type(do_compression("akaza.png")), str


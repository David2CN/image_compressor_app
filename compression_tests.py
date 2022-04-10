import pytest

from compressor import do_compression, read_image, compress

img_path = "static/images/akaza.png"

def test_read_image():
    assert read_image("hello"), "Invalid file type!, valid file types include:\
.jpg, .png, .jpeg, .gif, etc"
    # assert (type(read_image(img_path)), type())

def test_compress():
    img = read_image(img_path)
    assert type(compress(img)), type(img)

def test_do_compression():
    assert type(do_compression("akaza.png")), str


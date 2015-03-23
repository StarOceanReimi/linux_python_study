#!/usr/bin/python
import sys
from PIL import Image

def print_image_detail(image_filename):
    im = Image.open(infile)
    size = im.size
    print "%s, format=%s, imagesize=(%dx%d), mode=%s" % (infile, im.format, size[0], size[1], im.mode)

if len(sys.argv) == 1:
    for infile in sys.stdin:
        infile = infile.strip()
        if infile:
            print_image_detail(infile)

for infile in sys.argv[1:]:
    print_image_detail(infile)

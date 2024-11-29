import subprocess
import sys

from PIL import Image

x = 500
y = 100
files = [
    ["partial-input.png", None, "partial.png"],
    ["full-input.png", "clipboard-input.jpg", "full.png"],
    ["fixup-input.png", "np-input.png", "fixup.png"],
]


def comp(input1, input2, output):
    command = "magick", "-size", f"{ow}x{oh}", "xc:none", r"\t\transparent.png"
    subprocess.run(command, check=True)


def get_image_size(image_path):
    with Image.open(image_path) as img:
        return img.size  # Returns (width, height)


if __name__ == "__main__":
    width = 0
    height = 0
    for iio in files:
        input1, input2, output = iio
        if input2:
            width1, height1 = get_image_size(input2)
            width = max(width, width1)
            height = max(height, height1)
    ow = width + x
    oh = height + y
    for iio in files:
        input1, input2, output = iio
        comp(input1, input2, output)

import os
import subprocess
import sys

from PIL import Image

x = 400
y = 400
files = [
    ["partial.png", None, "partial.png"],
    ["full.png", "np.png", "full.png"],
    ["fixup.png", "np.png", "fixup.png"],
]


def comp(input1, input2, output):
    command = "magick", "-size", f"{ow}x{oh}", "xc:rgba(0,0,1,0)", r"\t\transparent.png"
    subprocess.run(command, check=True)

    command = (
        "magick",
        "composite",
        "-geometry",
        "+0+0",
        input1,
        r"\t\transparent.png",
        output,
    )
    subprocess.run(command, check=True)

    if input2:
        command = (
            "magick",
            "composite",
            "-geometry",
            f"+{x}+{y}",
            input2,
            output,
            output,
        )
        subprocess.run(command, check=True)


def get_image_size(image_path):
    with Image.open(image_path) as img:
        return img.size  # Returns (width, height)


if __name__ == "__main__":
    width = 0
    height = 0
    for iio in files:
        input1, input2, output = iio
        input1 = os.path.join("screenshots", input1)
        output = os.path.join("site", output)
        if input2:
            input2 = os.path.join("screenshots", input2)
            width1, height1 = get_image_size(input2)
            width = max(width, width1)
            height = max(height, height1)
    ow = width + x
    oh = height + y
    for iio in files:
        input1, input2, output = iio
        input1 = os.path.join("screenshots", input1)
        output = os.path.join("site", output)
        if input2:
            input2 = os.path.join("screenshots", input2)
        comp(input1, input2, output)

import subprocess
import sys

from PIL import Image

x = 500
y = 100
files = [["partial-input.png", None, "partial.png"]]


def comp(input1, input2, output):
    # Get the size of the existing image
    width, height = get_image_size(image_path)

    # Construct and execute the ImageMagick command
    command = ["magick", "-size", f"{width}x{height}", "xc:none", output_filename]
    subprocess.run(command, check=True)
    print(f"Transparent canvas created: {output_filename}")


def get_image_size(image_path):
    with Image.open(image_path) as img:
        return img.size  # Returns (width, height)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_canvas_from_image.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    create_transparent_canvas(image_path)

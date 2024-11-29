import subprocess
import sys
from PIL import Image

def get_image_size(image_path):
    with Image.open(image_path) as img:
        return img.size  # Returns (width, height)

def create_transparent_canvas(image_path, output_filename='transparent.png'):
    try:
        # Get the size of the existing image
        width, height = get_image_size(image_path)
        
        # Construct and execute the ImageMagick command
        command = ['magick', 'convert','-size', f'{width}x{height}', 'xc:none', output_filename]
        subprocess.run(command, check=True)
        print(f"Transparent canvas created: {output_filename}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_canvas_from_image.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    create_transparent_canvas(image_path)

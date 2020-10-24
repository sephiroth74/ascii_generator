import argparse
import os
import sys
from enum import Enum

import requests
from PIL import Image

sys.path.append(os.path.dirname(__file__))

import logger

IMAGE_RATIO = 0.55
DEFAULT_CHAR = "@"

class ImageFormat(Enum):
    BW = "1"
    GREYSCALE = "L"
    PALETTE = "P"
    RGB = "RGB"

    def __str__(self):
        return self.value


class ConsoleColors:
    END = "\033[0m"


""" Process input arguments """


def process(arguments):
    image = fetch_image(arguments.source)

    logger.debug("Image Size:   %sx%s", image.size[0], image.size[1])
    logger.debug("Image Mode:   %s", image.mode)
    logger.debug("Image Format: %s", image.format)

    image = resize_image(image, arguments.width)

    logger.debug("New Image Size: %sx%s", image.size[0], image.size[1])
    image = convert_image(image, arguments.colors)

    file_buffer = print_image(image, arguments)

    if arguments.output:
        save_image(file_buffer, arguments.output)


""" Convert Image based on ImageFormat """


def convert_image(image, colors):
    logger.debug("Converting image to %s colors...", colors.value)

    if colors == ImageFormat.PALETTE:
        image = image.convert(colors.value, palette=Image.ADAPTIVE, colors=8)
    else:
        image = image.convert(colors.value)

    image = image.convert("RGB")
    return image


""" Resize the image based on the given width """


def resize_image(image, new_width):
    logger.debug("Resizing Image to %s...", new_width)
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * IMAGE_RATIO)
    return image.resize((new_width, int(new_height)))


""" Fetch local or remote source images """


def fetch_image(source):
    logger.debug("Fetching %s...", source)
    img = None
    if source.startswith("http") or source.startswith("https"):
        req = requests.get(source, stream=True)
        req.raw.decode_content = True
        img = Image.open(req.raw)
    else:
        img = Image.open(source)
    return img


""" Convert given color to console color """


def to_console_color(value, use_background=False):
    if use_background:
        return "\033[48;2;{};{};{}m".format(value[0], value[1], value[2])
    else:
        return "\033[38;2;{};{};{}m".format(value[0], value[1], value[2])


""" Print the image to output """


def print_image(image, arguments):
    logger.debug("Printing Image ASCII...")
    row_index = 0
    col_index = 0
    file_buffer = ""

    img_width = image.size[0]
    img_height = image.size[1]

    for row_index in range(0, img_height):
        buf = ConsoleColors.END
        old_pixel = None

        for col_index in range(0, img_width):
            pixel = image.getpixel((col_index, row_index))
            char = " " if pixel == (0, 0, 0) else arguments.char
            if pixel != old_pixel:
                buf += to_console_color(pixel, arguments.background) + char
            else:
                buf += char
            old_pixel = pixel

        file_buffer += buf + ConsoleColors.END + "\n"
        print(buf)

    return file_buffer


""" Save the image string buffer to file """


def save_image(file_buffer, output):
    file = os.path.abspath(output)
    logger.debug("Saving ascii image to %s...", file)

    with open(file, "w") as f:
        f.write(file_buffer)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("--width", type=int, default=120, help=("Image width"))
    parser.add_argument("--verbose", action="store_true")
    
    parser.add_argument(
        "--colors",
        type=ImageFormat,
        default=ImageFormat.RGB,
        help=("Color Space. Default is RGB"),
        choices=list(ImageFormat),
    )
    
    parser.add_argument(
        "--background",
        help=("If True, use background color instead of foreground"),
        action="store_true",
    )
    
    parser.add_argument(
        "--output", type=str, default=None, help=("Save the ASCII Image to file")
    )

    parser.add_argument(
        "--char",
        type=str,
        default=DEFAULT_CHAR,
        help=("Use the given char to print each pixel"),
    )

    args = parser.parse_args()

    if args.verbose:
        logger.set_logger_level(logger.logging.DEBUG)
    else:
        logger.set_logger_level(logger.logging.INFO)

    logger.debug("Source:     %s", args.source)
    logger.debug("Width:      %s", args.width)
    logger.debug("Colors:     %s", args.colors)
    logger.debug("Background: %s", args.background)
    logger.debug("Output:     %s", args.output)
    logger.debug("Char:       %s", args.char)

    try:
        process(args)
    except Exception as e:
        logger.error(e)

    sys.exit(0)    

"""
Entry Method
"""
if __name__ == "__main__":
    main()


import math
import os
import random

from PIL import Image, ImageDraw

import algorithm.bruteforce_check
from func.func import fit_to_segment


def to_grayscale(image):
    image = image.convert('RGB')
    pixels = image.load()
    drawer = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    for i in range(width):
        for j in range(height):
            a, b, c = pixels[i, j][0], pixels[i, j][1], pixels[i, j][2]
            s = (a + b + c) // 3
            drawer.point((i, j), (s, s, s))
    return image


def resize_image(image, width, height):
    return image.resize((width, height))


def add_noise(image, delta):
    pixels = image.load()
    drawer = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    for i in range(width):
        for j in range(height):
            rgb = [0, 0, 0]
            for k in range(3):
                rgb[k] = fit_to_segment(pixels[i, j][k] + random.randint(-delta, delta), 0, 255)
            drawer.point((i, j), tuple(rgb))
    return image


def is_supported_image_extension(path):
    try:
        image = Image.open(path)
        image.close()
    except OSError:
        return False
    return True


def is_images_equal(first, second, resize_coefficient):
    """
    :param first: path to first image
    :param second: path to second image
    :param resize_coefficient: number ∈ [0;1]
    :return: true if images equal or false instead
    """
    if first == second:
        return True
    first_image = Image.open(first)
    second_image = Image.open(second)
    if resize_coefficient < 0 or resize_coefficient > 1:
        raise Exception('expected coefficient ∈ [0;1]')
    first_image = resize_image(first_image,
                               max(10, math.floor(first_image.size[0] * resize_coefficient)),
                               max(10, math.floor(first_image.size[1] * resize_coefficient)))
    second_image = resize_image(second_image,
                                max(10, math.floor(second_image.size[0] * resize_coefficient)),
                                max(10, math.floor(second_image.size[1] * resize_coefficient)))
    return algorithm.bruteforce_check.compare_images(first_image, second_image)


def collect_images(path, should_go_deeper):
    addresses_of_images = []
    if os.path.isdir(path):
        for address, dirs, files in os.walk(path):
            for file in files:
                cur_address = address + '/' + file
                try:
                    image = Image.open(cur_address)
                except OSError:
                    continue
                addresses_of_images.append(cur_address)
            if not should_go_deeper:
                return addresses_of_images
    elif os.path.isfile(path):
        try:
            image = Image.open(path)
        except OSError:
            return []
        addresses_of_images.append(path)
    else:
        return None
    return addresses_of_images

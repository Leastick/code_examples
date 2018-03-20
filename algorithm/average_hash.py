from PIL import ImageDraw

from func.image_func import to_grayscale, resize_image

HEIGHT = 16
WIDTH = 16
DELTA_X = 0
DELTA_Y = 0
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def calculate_average(x, y, image):
    pixels = image.load()
    color_sum = [0, 0, 0]
    counter = 0
    for i in range(x - DELTA_X, x + DELTA_X + 1):
        for j in range(y - DELTA_Y, y + DELTA_Y + 1):
            if WIDTH > i >= 0 and HEIGHT > j >= 0:
                for k in range(3):
                    color_sum[k] += pixels[i, j][k]
                counter += 1
    for i in range(3):
        color_sum[i] /= counter
    return sum(color_sum)


def pixel_averaging(image):
    width = image.size[0]
    height = image.size[1]
    average = [[0 for _ in range(height)] for _ in range(width)]
    for i in range(WIDTH):
        for j in range(HEIGHT):
            average[i][j] = calculate_average(i, j, image)
    return average


def should_pixel_be_black(average):
    return average < 127 * 3


def simplify_colors(image):
    average = pixel_averaging(image)
    drawer = ImageDraw.Draw(image)
    for i in range(WIDTH):
        for j in range(HEIGHT):
            drawer.point((i, j),
                         BLACK if should_pixel_be_black(average[i][j]) else WHITE)
    return image


def calculate_hash(image):
    image = simplify_colors(to_grayscale(resize_image(image, WIDTH, HEIGHT)))
    image_hash = 0
    pixels = image.load()
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if pixels[i, j][0] == 0:
                image_hash += 2 ** ((i * WIDTH) + j)
    return image_hash

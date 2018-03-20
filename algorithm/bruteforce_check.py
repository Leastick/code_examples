def compare_images(first_image, second_image):
    if first_image.size[0] != second_image.size[0] or \
                    first_image.size[1] != second_image.size[1]:
        return False
    width, height = first_image.size
    pixels_first = first_image.load()
    pixels_second = second_image.load()
    for i in range(width):
        for j in range(height):
            for k in range(3):
                if pixels_first[i, j][k] != pixels_second[i, j][k]:
                    return False
    return True

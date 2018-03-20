import os
import random
import unittest
import func.func
import func.image_func
import algorithm.average_hash

from PIL import Image, ImageDraw

from algorithm.bruteforce_check import compare_images

PATH = os.getcwd() + '/pics/testing_pictures'


class AverageHashTest(unittest.TestCase):

    @staticmethod
    def generate_random_grayscale_image():
        image = Image.open(PATH + '/cactus.jpg')
        image = func.image_func.resize_image(image, 16, 16)
        width = image.size[0]
        height = image.size[1]
        drawer = ImageDraw.Draw(image)
        for i in range(width):
            for j in range(height):
                color = random.randint(0, 256)
                drawer.point((i, j), (color, color, color))
        return image

    def test_calculate_hash_simple(self):
        for k in range(0, 1000):
            image = self.generate_random_grayscale_image()
            image_hash = algorithm.average_hash.calculate_hash(image)
            width = image.size[0]
            height = image.size[1]
            expected_hash = 0
            for i in range(width):
                for j in range(height):
                    average = algorithm.average_hash.calculate_average(i, j, image)
                    if algorithm.average_hash.should_pixel_be_black(average):
                        expected_hash += 2 ** (i * width + j)
            self.assertEqual(expected_hash, image_hash)


class BruteforceTest(unittest.TestCase):

    def test_with_equal_images(self):
        image1 = Image.open(PATH + '/cactus.jpg')
        image2 = Image.open(PATH + '/cactus1.jpg')
        self.assertTrue(compare_images(image1, image2))

    def test_with_different_images(self):
        image1 = Image.open(PATH + '/stellar_sky.jpg')
        image2 = Image.open(PATH + '/cactus.jpg')
        self.assertFalse(compare_images(image1, image2))

    def test_with_similar_images(self):
        image1 = Image.open(PATH + '/noise_level_10_cactus.jpg')
        image2 = Image.open(PATH + '/cactus.jpg')
        self.assertFalse(compare_images(image1, image2))

    def test_with_same_image(self):
        image1 = Image.open(PATH + '/stellar_sky.jpg')
        image2 = Image.open(PATH + '/stellar_sky.jpg')
        self.assertTrue(compare_images(image1, image2))


class FuncTest(unittest.TestCase):

    def test_resize(self):
        image = Image.open(PATH + '/cactus.jpg')
        for i in range(1, 100):
            for j in range(1, 100):
                image = func.image_func.resize_image(image, i, j)
                self.assertEquals((i, j), (image.size[0], image.size[1]))

    def test_to_grayscale(self):
        image = Image.open(PATH + '/cactus.jpg')
        image = func.image_func.to_grayscale(image)
        pixels = image.load()
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                self.assertTrue(pixels[i, j][0] == pixels[i, j][1] == pixels[i, j][2])

    def test_is_images_equal(self):
        first = PATH + '/cactus.jpg'
        second = PATH + '/cactus1.jpg'
        self.assertTrue(func.image_func.is_images_equal(first, second, 1))
        self.assertTrue(func.image_func.is_images_equal(first, second, 0.5))
        first = PATH + '/cactus.jpg'
        second = PATH + '/noise_level_10_cactus.jpg'
        self.assertFalse(func.image_func.is_images_equal(first, second, 1))
        self.assertFalse(func.image_func.is_images_equal(first, second, 0.5))

    def test_image_collector(self):
        path = PATH[:-17]
        collected_got = func.image_func.collect_images(path, False)
        collected_expected = []
        for address, directories, files in os.walk(path):
            for file in files:
                if func.image_func.is_supported_image_extension('{0}/{1}'.format(address, file)):
                    collected_expected.append('{0}/{1}'.format(address, file))
            break
        self.assertEqual(collected_expected, collected_got)
        collected_got = func.image_func.collect_images(path, True)
        collected_expected = []
        for address, directories, files in os.walk(path):
            for file in files:
                if func.image_func.is_supported_image_extension('{0}/{1}'.format(address, file)):
                    collected_expected.append('{0}/{1}'.format(address, file))
        self.assertEqual(collected_expected, collected_got)

    def test_try_parse_int(self):
        self.assertTrue(func.func.tryparse_int('aaaaaa') is None)
        self.assertTrue(func.func.tryparse_int('12.34a5') is None)
        self.assertTrue(func.func.tryparse_int('12.345') is None)
        self.assertEqual(func.func.tryparse_int('12'), 12)
        self.assertEqual(func.func.tryparse_int('-12'), -12)
        self.assertEqual(func.func.tryparse_int('012'), 12)
        self.assertEqual(func.func.tryparse_int('+12'), 12)

    def try_parse_float(self):
        self.assertTrue(func.func.tryparse_float('aaaaaa') is None)
        self.assertTrue(func.func.tryparse_float('12.34a5') is None)
        self.assertEqual(func.func.tryparse_float('12.222'), 12.222)
        self.assertEqual(func.func.tryparse_float('-12.222'), -12.222)
        self.assertEqual(func.func.tryparse_float('0012.222'), 12.222)
        self.assertEqual(func.func.tryparse_float('+12.222'), 12.222)
        self.assertEqual(func.func.tryparse_float('12'), 12.0)


if __name__ == '__main__':
    unittest.main()

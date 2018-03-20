import math

import exifread
from PIL import Image

from algorithm.average_hash import calculate_hash
from func.func import hamming_distance, tryfind
from func.image_func import is_images_equal


class Album:
    def __init__(self, name):
        self.images_path = []
        self.from_image_to_hash = dict()
        self.album_name = name
        self.image_index = 0
        self.from_image_to_exif = dict()
        self.is_clustered = False
        self.acceptable_hamming_distance = 5
        self.MAX_HAMMING_DISTANCE = 15
        self.equality_coefficient = 0.1

    def rename_album(self, name):
        self.album_name = name

    def add_image(self, path):
        if path not in self.images_path:
            if self.is_clustered:
                image_hash = self.get_image_hash(path)
                self.from_image_to_hash[path] = image_hash
            with open(path, 'rb') as f:
                self.from_image_to_exif[path] = exifread.process_file(f)
            self.images_path.append(path)
            self.images_path.sort()

    def remove_image(self, path):
        index = tryfind(self.images_path, path)
        if index is None:
            return
        if self.image_index >= index:
            self.image_index -= 1
        if self.is_clustered:
            self.from_image_to_hash.pop(path)
        self.images_path.remove(path)

    def __iter__(self):
        return iter(self.images_path)

    def next_image(self):
        modulo = len(self.images_path)
        self.image_index = (self.image_index + 1) % modulo
        return self.images_path[self.image_index]

    def prev_image(self):
        modulo = len(self.images_path)
        self.image_index = (self.image_index - 1 + modulo) % modulo
        return self.images_path[self.image_index]

    def current_image(self):
        if len(self.images_path) == 0:
            return None
        return self.images_path[self.image_index]

    def is_empty(self):
        return len(self.images_path) == 0

    def make_clustering(self):
        self.is_clustered = True
        for image_path in self.images_path:
            with Image.open(image_path) as image:
                self.from_image_to_hash[image_path] = self.get_image_hash(image_path)

    @staticmethod
    def get_image_hash(path):
        with Image.open(path) as image:
            return calculate_hash(image)

    def find_similar_to_this_images(self, path):
        if not self.is_clustered:
            self.make_clustering()
        hash_image = Album.get_image_hash(path)
        with_similar_hashes = set()
        similar = Album('Images similar to ' + path)
        for key in self.from_image_to_hash:
            if key == path and key not in with_similar_hashes:
                with_similar_hashes.add(key)
            elif hamming_distance(self.from_image_to_hash[key], hash_image) \
                    <= self.acceptable_hamming_distance:
                with_similar_hashes.add(key)
        for item in with_similar_hashes:
            similar.add_image(item)
        return similar

    def delete_duplicates(self):
        for_deleting = []
        for i in range(len(self.images_path)):
            for j in range(i + 1, len(self.images_path)):
                if self.from_image_to_hash[self.images_path[i]] == \
                        self.from_image_to_hash[self.images_path[j]]:
                    if is_images_equal(self.images_path[i],
                                       self.images_path[j],
                                       self.equality_coefficient):
                        for_deleting.append(self.images_path[j])
        for path in for_deleting:
            self.remove_image(path)

    def change_similarity_coefficient(self, coefficient):
        self.acceptable_hamming_distance = max(1, math.floor(self.MAX_HAMMING_DISTANCE *
                                                             coefficient))

    def change_equality_coefficient(self, coefficient):
        self.equality_coefficient = coefficient

    def remove_images_that_does_not_exist(self):
        for_deleting = []
        for path in self.images_path:
            try:
                file = open(path)
                file.close()
            except IOError as e:
                for_deleting.append(path)
        for path in for_deleting:
            self.remove_image(path)

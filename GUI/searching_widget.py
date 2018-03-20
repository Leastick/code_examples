import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QGridLayout, QFileDialog,
                             QToolButton, QInputDialog, QDialog,
                             QMessageBox)

from GUI.image_show_window import ImageShowWindow
from func.func import tryparse_float
from func.image_func import is_supported_image_extension

PATH = os.getcwd()
SHIFT = 5


class SearchingMenuWidget(QDialog):
    def __init__(self, album, width, height):
        super(SearchingMenuWidget, self).__init__()
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.album = album
        self.__init_UI()

    def __init_UI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setWindowTitle(self.album.album_name)
        self.setFixedSize(200, 350)

        delete_duplicates_action = QAction('Delete duplicates', self)
        delete_duplicates_action.setToolTip('Delete equal images from album')
        delete_duplicates_action.triggered.connect(self.album.delete_duplicates)

        delete_duplicates_btn = QToolButton(self)
        delete_duplicates_btn.setDefaultAction(delete_duplicates_action)

        find_similar_action = QAction('Find similar', self)
        find_similar_action.setToolTip('Find images similar to specified image')
        find_similar_action.triggered.connect(self.find_similar)

        find_similar_btn = QToolButton(self)
        find_similar_btn.setDefaultAction(find_similar_action)

        change_equality_coefficient_action = QAction(QIcon(PATH + '/pics/settings_icon.png'),
                                                     'Change equality coefficient', self)
        change_equality_coefficient_action.setToolTip('Change coefficient that using for ' +
                                                      'finding equal images')
        change_equality_coefficient_action.triggered.connect(self.change_equality_coefficient)

        change_equality_coefficient_btn = QToolButton(self)
        change_equality_coefficient_btn.setDefaultAction(change_equality_coefficient_action)

        change_similarity_coefficient_action = QAction(QIcon(
            PATH + '/pics/settings_icon.png'),
            'Change similarity coefficient',
            self)
        change_similarity_coefficient_action.setToolTip(
            'Change coefficient that using for finding similar images')
        change_similarity_coefficient_action.triggered.connect(self.change_similarity_coefficient)

        change_similarity_coefficient_btn = QToolButton(self)
        change_similarity_coefficient_btn.setDefaultAction(change_similarity_coefficient_action)


        back_action = QAction('Back', self)
        back_action.triggered.connect(self.close)

        back_btn = QToolButton(self)
        back_btn.setDefaultAction(back_action)

        self.grid.addWidget(delete_duplicates_btn, 0, 0)
        self.grid.addWidget(change_equality_coefficient_btn, 0, 1)
        self.grid.addWidget(find_similar_btn, 1, 0)
        self.grid.addWidget(change_similarity_coefficient_btn, 1, 1)
        self.grid.addWidget(back_btn, 2, 0)

        self.show()

    def change_equality_coefficient(self):
        text, ok = QInputDialog.getText(self, 'Change equality coefficient',
                                        'Enter equality coefficient (from 0 to 1)\n' +
                                        'Current coefficient is {}'.format(
                                            self.album.equality_coefficient
                                        ))
        if ok and text is not None:
            k = tryparse_float(text)
            if k is None or k < 0 or k > 1:
                QMessageBox.warning(self, "Incorrect coefficient",
                                    "Expected coefficient ∈ [0;1]", QMessageBox.Ok)
            else:
                self.album.change_equality_coefficient(k)

    def change_similarity_coefficient(self):
        k = (self.album.acceptable_hamming_distance /
            self.album.MAX_HAMMING_DISTANCE)
        text, ok = QInputDialog.getText(self, 'Change similarity coefficient',
                                        'Enter similarity coefficient (from 0 to 1)\n' +
                                        'Current coefficient is {}'.format(k))
        if ok and text is not None:
            k = tryparse_float(text)
            if k is None or k < 0 or k > 1:
                QMessageBox.warning(self, "Incorrect coefficient",
                                    "Expected coefficient ∈ [0;1]", QMessageBox.Ok)
            else:
                self.album.change_similarity_coefficient(k)

    def find_similar(self):
        if self.album.is_empty():
            QMessageBox.warning(self, "Error",
                                "Album is empty", QMessageBox.Ok)
            return
        file_path = QFileDialog.getOpenFileName(self, 'Select file', '/home')[0]
        if file_path is not None and file_path != '':
            if is_supported_image_extension(file_path):
                similar_images = self.album.find_similar_to_this_images(file_path)
                if similar_images.is_empty():
                    return
                self.close()
                window = ImageShowWindow(similar_images, self.SCREEN_WIDTH,
                                         self.SCREEN_HEIGHT)
                window.move(0, 0)
                window.exec_()
            else:
                QMessageBox.warning(self, "Unsupported extension",
                                    "Select a supported file extension", QMessageBox.Ok)
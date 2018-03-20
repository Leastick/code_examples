import os
import subprocess
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QAction, QPushButton,
                             QGridLayout, QFileDialog, QToolButton,
                             QLabel, QScrollArea, QMessageBox)
from GUI.events import ChangeDirectory

from GUI.image_show_window import ImageShowWindow
from album import Album
from func.image_func import collect_images
from GUI.searching_widget import SearchingMenuWidget

PATH = os.getcwd()
SHIFT = 5


class NavigateWidget(QWidget):
    def __init__(self, parent, directory, width, height):
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        super(NavigateWidget, self).__init__(parent)
        self.current_directory = directory
        self.__init_UI(self.current_directory)

    def __init_UI(self, directory):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.actions = []
        self.__generate(directory)
        self.directoryChanger = ChangeDirectory()

        self.show()

    def change_directory(self, path):
        self.directoryChanger.directoryChanged.emit(path)
        self.current_directory = path
        self.__generate(path)

    def update_directory_without_notification(self, path):
        self.current_directory = path
        self.__generate(path)

    def __generate(self, directory):
        self.__clean_layout()
        self.actions = []
        line_number = SHIFT
        for path, dirs, files in os.walk(directory):
            if len(files) > 0:
                file_label = QLabel('<b>Files:</b>', self)
                self.grid.addWidget(file_label, 0, 0, 1, 1)
            for file in files:
                new_button = QToolButton(self)
                filename = QLabel('<i>' + file + '</i>')
                self.grid.addWidget(new_button, line_number, 0, 5, 5)
                self.grid.addWidget(filename, line_number, 1, 5, 10)
                #new_button.setStyleSheet('border: none;')

                action = QAction(QIcon(PATH + '/pics/file_icon.png'), 'Open file ' + file, self)
                file_path = path + '/' + file
                action.triggered.connect(lambda checked, file_path=file_path: self.open_file(file_path))
                self.actions.append(action)
                new_button.setDefaultAction(action)
                line_number += SHIFT
            if len(dirs) > 0:
                dir_label = QLabel('<b>Directories:</b>', self)
                self.grid.addWidget(dir_label, line_number, 0, 1, 1)
                line_number += SHIFT
            for directory_name in dirs:
                new_button = QToolButton(self)
                directory_label = QLabel('<i>' + directory_name + '</i>')
                self.grid.addWidget(new_button, line_number, 0, 5, 5)
                self.grid.addWidget(directory_label, line_number, 1, 5, 10)
                line_number += SHIFT

                action = QAction(QIcon(PATH + '/pics/folder_icon.png'), 'Change directory to ' + directory_name, self)
                directory_path = path + '/' + directory_name
                action.triggered.connect(lambda checked,
                                                directory_path=directory_path:
                                         self.change_directory(directory_path))
                self.actions.append(action)
                new_button.setDefaultAction(action)

            break

    def __clean_layout(self):
        for i in reversed(range(self.grid.count())):
            widget_to_remove = self.grid.itemAt(i).widget()
            self.grid.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

    @staticmethod
    def open_file(path_file):
        if sys.platform == "win32":
            os.startfile(path_file)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, path_file])

    def show_images_from_directory(self):
        album = Album(self.current_directory.split('/')[-1])
        images = collect_images(self.current_directory, False)
        for path in images:
            album.add_image(path)
        if album.is_empty():
            QMessageBox.warning(self, "Error",
                                "There are no images in this folder", QMessageBox.Ok)
        else:
            image_opener = ImageShowWindow(album, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            image_opener.move(0, 0)
            image_opener.exec_()


class FileSystemWidget(QWidget):
    def __init__(self, parent, width, height):
        super(FileSystemWidget, self).__init__(parent)
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.current_directory = os.getcwd()
        self.__init_UI()

    def __init_UI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        choose_directory_btn = QPushButton('Change directory', self)
        choose_directory_btn.setToolTip('Chose current directory')
        choose_directory_btn.clicked.connect(self.show_dialog)

        self.label = QLabel('<b>Current directory:</b>' + self.current_directory, self)
        self.explorer = NavigateWidget(None, self.current_directory, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        show_images_btn = QPushButton('Show images', self)
        show_images_btn.clicked.connect(self.explorer.show_images_from_directory)

        clustering_btn = QPushButton('Clustering menu', self)
        clustering_btn.clicked.connect(self.open_clustering_menu)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.explorer)

        grid.addWidget(self.label, 0, 1, 1, 1)
        grid.addWidget(choose_directory_btn, 0, 10, 1, 1)
        grid.addWidget(show_images_btn, 11, 1, 1, 1)
        grid.addWidget(clustering_btn, 11, 2, 1, 1)
        grid.addWidget(scroll_area, 1, 1, 10, 10)

        self.explorer.directoryChanger.directoryChanged.connect(self.change_directory)
        self.show()

    def open_clustering_menu(self):
        album = Album('{0}_temp_album'.format(self.current_directory.rsplit('/', maxsplit=1)[1]))
        images = collect_images(self.current_directory, False)
        for path in images:
            album.add_image(path)
        album.make_clustering()
        window = SearchingMenuWidget(album, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        window.exec_()

    def update_current_directory_line(self):
        if len(self.current_directory) <= 220:
            self.label.setText('<b>Current directory: </b>' + self.current_directory)
        else:
            self.label.setText('<b>Current directory: </b>' + self.current_directory[-220:])

    def show_dialog(self):
        directory = QFileDialog.getExistingDirectory(self, 'Change directory', '/home')
        if directory != '':
            self.current_directory = directory
            self.explorer.change_directory(directory)
        self.update_current_directory_line()

    def change_directory(self, path):
        self.current_directory = path
        self.update_current_directory_line()

    def go_to_upper_directory(self):
        if self.current_directory[len(self.current_directory) - 1] == '/':
            self.current_directory = self.current_directory[:-1]
        index = self.current_directory.rfind('/')
        if index != 0:
            new_directory = self.current_directory[:index]
            self.change_directory(new_directory)
            self.explorer.update_directory_without_notification(new_directory)

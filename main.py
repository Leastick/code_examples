import _pickle as pickle
import os
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from GUI.main_window import MainWindow

PATH = os.getcwd()
SHIFT = 5


def save(window):
    with open(PATH + '/data/screen_width_data.pkl', 'wb') as f:
        pickle.dump(window.main_widget.file_system_widget.SCREEN_WIDTH, f, 2)
    with open(PATH + '/data/screen_height_data.pkl', 'wb') as f:
        pickle.dump(window.main_widget.file_system_widget.SCREEN_HEIGHT, f, 2)
    with open(PATH + '/data/album_data.pkl', 'wb') as f:
        pickle.dump(window.main_widget.album_widget.explorer.albums, f, 2)


def load():
    try:
        with open(PATH + '/data/screen_width_data.pkl', 'rb') as f:
            width = pickle.load(f)
        with open(PATH + '/data/screen_height_data.pkl', 'rb') as f:
            height = pickle.load(f)
        with open(PATH + '/data/album_data.pkl', 'rb') as f:
            albums = pickle.load(f)
    except FileNotFoundError:
        return MainWindow()
    window = MainWindow(width, height)
    window.main_widget.album_widget.explorer.albums = albums
    for album in window.main_widget.album_widget.explorer.albums:
        album.remove_images_that_does_not_exist()
    window.main_widget.album_widget.explorer.redraw()
    return window


def main():
    app = QApplication(sys.argv)
    window = load()
    window.save_event.dataSaved.connect(lambda data=window: save(data))
    directory = PATH + '/pics/logo.png'
    app.setWindowIcon(QIcon(directory))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

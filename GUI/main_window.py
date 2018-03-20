import sys

from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton,
                             QGridLayout, QInputDialog)
from GUI.events import ChangeMode, DataSaved
from GUI.file_system_mode import FileSystemWidget

from GUI.album_mode import AlbumWidget
from func.func import tryparse_int


class MainWidget(QWidget):
    def __init__(self, parent, width=None, height=None):
        super(MainWidget, self).__init__(parent)
        self.is_album_mode = True
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        if self.SCREEN_HEIGHT is None:
            self.update_resolution()
        self.__init_UI()

    def __init_UI(self):
        self.setGeometry(100, 100, 700, 400)
        grid = QGridLayout()
        self.setLayout(grid)
        self.modes = ChangeMode()
        self.save_event = DataSaved()

        self.back_btn = QPushButton('Go upper', self)
        self.back_btn.hide()
        self.back_btn.clicked.connect(self.back_btn_clicked)
        grid.addWidget(self.back_btn, 1, 0, 2, 1)

        mode_button = QPushButton('to File system mode', self)
        mode_button.resize(mode_button.sizeHint())
        grid.addWidget(mode_button, 0, 0, 1, 1)
        mode_button.clicked.connect(self.change_mode)
        mode_button.setToolTip('Change mode to ' + mode_button.text()[3:])

        save_btn = QPushButton('Save', self)
        save_btn.resize(save_btn.sizeHint())
        grid.addWidget(save_btn)
        save_btn.clicked.connect(self.save_data)

        self.file_system_widget = FileSystemWidget(self, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.album_widget = AlbumWidget(self, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        grid.addWidget(self.file_system_widget, 0, 1, 10, 10)
        grid.addWidget(self.album_widget, 0, 1, 10, 10)
        self.album_widget.show()
        self.file_system_widget.hide()

        self.show()

    def save_data(self):
        self.save_event.dataSaved.emit()

    def change_mode(self):
        self.modes.modeChanged.emit(not self.is_album_mode)
        if self.is_album_mode:
            self.sender().setText('to Album mode')
            self.back_btn.show()
            self.back_btn.setToolTip('Go to the upper directory')
            self.is_album_mode = False
            self.file_system_widget.show()
            self.album_widget.hide()
        else:
            self.sender().setText('to File system mode')
            self.back_btn.hide()
            self.is_album_mode = True
            self.album_widget.show()
            self.file_system_widget.hide()
        self.sender().setToolTip('Change mode to <i>' + self.sender().text()[3:] + '</i>')

    def back_btn_clicked(self):
        if not self.is_album_mode:
            self.file_system_widget.go_to_upper_directory()

    def update_resolution(self):
        while True:
            text, ok = QInputDialog.getText(self, 'Specify your screen resolution',
                                            'Please, use following format: <i>width+height</i>'
                                            "('+' is delimiter)")
            if not ok:
                sys.exit(0)
            resolution = text.split('+')
            if len(resolution) != 2:
                continue
            width = tryparse_int(resolution[0])
            height = tryparse_int(resolution[1])
            if width is None or height is None:
                continue
            self.SCREEN_WIDTH = width - 100
            self.SCREEN_HEIGHT = height - 100
            break


class MainWindow(QMainWindow):
    def __init__(self, width=None, height=None):
        super().__init__()
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.__init_UI()

    def __init_UI(self):
        self.setGeometry(100, 100, 700, 400)
        self.setWindowTitle('photoAlbum')
        self.statusBar().showMessage('Now in Album mode')
        self.save_event = DataSaved()

        self.main_widget = MainWidget(self, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.setCentralWidget(self.main_widget)
        self.main_widget.modes.modeChanged.connect(self.change_mode)
        self.main_widget.save_event.dataSaved.connect(self.save_data)

        self.show()

    def change_mode(self, is_album_mode):
        if not is_album_mode:
            self.statusBar().showMessage('Now in File system mode')
        else:
            self.statusBar().showMessage('Now in Album mode')

    def save_data(self):
        self.save_event.dataSaved.emit()

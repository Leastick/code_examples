from PyQt5.QtWidgets import (QVBoxLayout, QDialog, QLabel, QScrollArea,
                             QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import math


class ImageShowWindow(QDialog):
    def __init__(self, album, width, height):
        super(ImageShowWindow, self).__init__()
        self.SCREEN_HEIGHT = height
        self.SCREEN_WIDTH = width
        self.album = album
        self.current_image_path = self.album.current_image()
        self.box = QVBoxLayout()
        self.setLayout(self.box)
        self.should_scale = True
        self.__init_UI()

    def __init_UI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.__redraw()

    def __redraw(self):
        self.__clean_layout()
        image_name = self.current_image_path.split('/')[-1]
        label = QLabel(self)
        pixmap = QPixmap(self.current_image_path)
        if pixmap.isNull():
            self.setGeometry(0, 0, 20, 10)
            label.setText('Error occurred while opening')
            self.box.addWidget(label)
            return
        if self.should_scale:
            w_coef = min(self.SCREEN_WIDTH / pixmap.width(), 1)
            h_coef = min(self.SCREEN_HEIGHT / pixmap.height(), 1)
            coef = min(w_coef, h_coef)
            pixmap = pixmap.scaled(int(math.floor(pixmap.width() * coef)),
                                   int(math.floor(pixmap.height() * coef)))
            #self.setGeometry(0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            self.setWindowTitle(image_name)
            self.box.addWidget(label, 0)
            label.setPixmap(pixmap)
        else:
            scroll_area = QScrollArea()
            label.setPixmap(pixmap)
            scroll_area.setWidget(label)
            #self.setGeometry(0, 0,  self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            self.box.addWidget(scroll_area)
        self.setGeometry(0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.showFullScreen()

    def __clean_layout(self):
        for i in reversed(range(self.box.count())):
            widget_to_remove = self.box.itemAt(i).widget()
            self.box.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Left:
            self.current_image_path = self.album.prev_image()
            self.__redraw()
            self.releaseKeyboard()
        elif QKeyEvent.key() == Qt.Key_Right:
            self.current_image_path = self.album.next_image()
            self.__redraw()
        elif QKeyEvent.key() == Qt.Key_Escape:
            self.close()
        elif QKeyEvent.key() == Qt.Key_C:
            self.should_scale = not self.should_scale
            self.__redraw()

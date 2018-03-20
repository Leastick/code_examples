import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QAction, QPushButton,
                             QGridLayout, QFileDialog, QToolButton,
                             QLabel, QScrollArea, QInputDialog,
                             QVBoxLayout, QDialog,
                             QMessageBox, QCheckBox)
from GUI.events import (AlbumNameChanged, AlbumDeleted,
                            AlbumClustered)

from GUI.image_show_window import ImageShowWindow
from album import Album
from func.image_func import collect_images
from GUI.searching_widget import SearchingMenuWidget

PATH = os.getcwd()
SHIFT = 5


class EditAlbumWidget(QDialog):
    def __init__(self, album, width, height):
        super(EditAlbumWidget, self).__init__()
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.album = album
        self.__init_UI()

    def __init_UI(self):
        self.clustering_happened = AlbumClustered()
        self.box = QVBoxLayout()
        self.setLayout(self.box)
        self.setWindowTitle(self.album.album_name + ' menu')
        self.setFixedSize(150, 300)

        self.name_changed = AlbumNameChanged()
        self.album_deleted = AlbumDeleted()

        album_opener = QAction('Show images', self)
        album_opener.setToolTip('Showing images from this album')
        album_opener.triggered.connect(self.open_album)

        open_album_btn = QToolButton(self)
        open_album_btn.setDefaultAction(album_opener)

        album_deleter = QAction('Delete album', self)
        album_deleter.setToolTip('Delete this album')
        album_deleter.triggered.connect(self.delete_album)

        delete_album_btn = QToolButton(self)
        delete_album_btn.setDefaultAction(album_deleter)

        album_renamer = QAction('Rename album', self)
        album_renamer.setToolTip('Rename this album')
        album_renamer.triggered.connect(self.rename_album)

        rename_album_btn = QToolButton(self)
        rename_album_btn.setDefaultAction(album_renamer)

        images_adder = QAction('Add images', self)
        images_adder.setToolTip('Add images to this album')
        images_adder.triggered.connect(self.add_images_menu)

        add_images_btn = QToolButton(self)
        add_images_btn.setDefaultAction(images_adder)

        images_deleter = QAction('Delete images', self)
        images_deleter.setToolTip('Delete selected images')
        images_deleter.triggered.connect(self.delete_images)

        delete_images_btn = QToolButton(self)
        delete_images_btn.setDefaultAction(images_deleter)

        back = QAction('Back', self)
        back.setToolTip('Close this menu')
        back.triggered.connect(self.close)

        back_btn = QToolButton(self)
        back_btn.setDefaultAction(back)

        create_clustering = QAction('Do clustering')
        create_clustering.setToolTip('Create clusterization of this album')
        create_clustering.triggered.connect(self.create_clusterization)

        clustering_btn = QToolButton(self)
        clustering_btn.setDefaultAction(create_clustering)

        self.box.addWidget(open_album_btn, 0)
        self.box.addWidget(delete_album_btn, 1)
        self.box.addWidget(rename_album_btn, 2)
        self.box.addWidget(add_images_btn, 3)
        self.box.addWidget(delete_images_btn, 4)
        self.box.addWidget(clustering_btn, 5)
        self.box.addWidget(back_btn, 6)

        self.show()

    def create_clusterization(self):
        if not self.album.is_clustered:
            self.album.make_clustering()
            self.clustering_happened.albumClustered.emit()
        else:
            QMessageBox.warning(self, "Album clustered",
                                "Already clustered", QMessageBox.Ok)

    def open_album(self):
        self.close()
        if self.album.is_empty():
            QMessageBox.warning(self, "Cannot open album",
                                "There are no images in this album", QMessageBox.Ok)
        else:
            image_opener = ImageShowWindow(self.album, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            image_opener.move(0, 0)
            image_opener.exec_()

    def delete_album(self):
        should_delete = QMessageBox.question(self, 'Deleting album', 'Do you want to delete this album?',
                                             QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.No)
        if should_delete == QMessageBox.Yes:
            self.album_deleted.albumDeleted.emit(self.album.album_name)
            self.close()

    def rename_album(self):
        text, ok = QInputDialog.getText(self, 'Input dialog', 'Enter album new name')
        if ok and text is not None and text != '' and text != self.album.album_name:
            self.name_changed.nameChanged.emit(self.album.album_name, text)

    def add_images_menu(self):
        window = QDialog()
        window.setWindowTitle('Add images')
        window.setFixedSize(300, 200)
        window.setWindowFlags(Qt.WindowMinimizeButtonHint)

        box = QVBoxLayout()
        window.setLayout(box)

        select_file = QPushButton('Add file', window)
        select_directory = QPushButton('Add from directory', window)
        select_directory_and_subdirs = QPushButton('Add from directory and subdirectories', window)
        back = QPushButton('Back', window)

        back.clicked.connect(window.close)
        select_file.clicked.connect(self.add_images_from_file)
        select_directory.clicked.connect(self.add_images_from_directory)
        select_directory_and_subdirs.clicked.connect(self.add_images_from_directory_and_subdirectories)

        select_file.setAutoDefault(False)
        select_directory.setAutoDefault(False)
        select_directory_and_subdirs.setAutoDefault(False)
        back.setAutoDefault(False)
        box.addWidget(select_file, 0)
        box.addWidget(select_directory, 1)
        box.addWidget(select_directory_and_subdirs, 2)
        box.addWidget(back, 3)
        window.exec_()

    def add_images_from_file(self):
        file_path = QFileDialog.getOpenFileName(self, 'Select file', '/home')[0]
        self.add_images(collect_images(file_path, False), self.album)

    def add_images_from_directory(self):
        directory_path = QFileDialog.getExistingDirectory(self, 'Select directory', '/home')
        self.add_images(collect_images(directory_path, False), self.album)

    def add_images_from_directory_and_subdirectories(self):
        directory_path = QFileDialog.getExistingDirectory(self, 'Select directory', '/home')
        self.add_images(collect_images(directory_path, True), self.album)

    @staticmethod
    def add_images(images_path, album):
        if images_path is not None:
            for image_path in images_path:
                album.add_image(image_path)

    def delete_images(self):
        window = QDialog()
        window.setWindowTitle('Delete images')
        window.setFixedSize(500, 300)
        window.setWindowFlags(Qt.WindowMinimizeButtonHint)
        window.checkboxes = []

        checkbox_widget = QWidget(window)
        additional_layout = QVBoxLayout()
        checkbox_widget.setLayout(additional_layout)

        grid = QGridLayout()
        window.setLayout(grid)

        ok = QPushButton('OK', window)
        ok.setAutoDefault(False)
        cancel = QPushButton('Cancel', window)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(checkbox_widget)

        checkbox_all = QCheckBox('All', window)
        checkbox_all.setToolTip('Select all images')

        additional_layout.addWidget(checkbox_all, 0)
        window.checkboxes.append(checkbox_all)

        line_number = 1
        for file in self.album:
            checkbox = QCheckBox(file.split('/')[-1], window)
            checkbox.setToolTip(file)
            window.checkboxes.append(checkbox)
            additional_layout.addWidget(checkbox, line_number)
            checkbox.stateChanged.connect(lambda checked, x=checkbox_all: self.process_usual_checkbox(x))
            line_number += 1

        cancel.clicked.connect(window.close)
        checkbox_all.stateChanged.connect(lambda checked, x=window.checkboxes: self.chose_all_or_nothing(x))
        ok.clicked.connect(lambda checked, x=window.checkboxes, y=window: self.delete_chosen_images(x, y))

        grid.addWidget(ok, 0, 0)
        grid.addWidget(cancel, 1, 0)
        grid.addWidget(scroll_area, 0, 1, 10, 10)

        window.exec_()

    def delete_chosen_images(self, checkboxes, window):
        for checkbox in checkboxes:
            if checkbox.text() != 'All' and checkbox.isChecked():
                self.album.remove_image(checkbox.toolTip())
        window.close()

    def chose_all_or_nothing(self, checkboxes):
        if self.sender().isChecked():
            for checkbox in checkboxes:
                checkbox.setChecked(True)
        else:
            for checkbox in checkboxes:
                checkbox.setChecked(False)

    def process_usual_checkbox(self, all_checkbox):
        all_checkbox.blockSignals(True)
        if not self.sender().isChecked():
            all_checkbox.setChecked(False)
        all_checkbox.blockSignals(False)


class AlbumNavigateWidget(QWidget):
    def __init__(self, parent, width, height):
        super(AlbumNavigateWidget, self).__init__(parent)
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.albums = []
        self.__init_UI()

    def __init_UI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.show()

    def __clean_layout(self):
        for i in reversed(range(self.grid.count())):
            widget_to_remove = self.grid.itemAt(i).widget()
            self.grid.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

    def create_album(self):
        new_album_name = self.show_dialog()
        if new_album_name is not None:
            for album in self.albums:
                if album.album_name == new_album_name:
                    return
            self.albums.append(Album(new_album_name))
            self.redraw()

    def show_dialog(self):
        text, ok = QInputDialog.getText(self, 'Input dialog', 'Enter album name')
        return text if ok else None

    def redraw(self):
        self.__clean_layout()
        line_number = 0
        for album in self.albums:
            name_of_the_album = album.album_name
            album_label = QLabel(name_of_the_album, self)
            edit_menu_btn = QToolButton(self)

            action = QAction(QIcon(PATH + '/pics/photoalbum_icon.png'), 'Open image menu', self)
            action.triggered.connect(lambda checked,
                                            current_album=album:
                                     self.open_edit_menu(current_album))
            edit_menu_btn.setDefaultAction(action)

            clustering_action = QAction(QIcon(PATH + '/pics/searcher_icon.png'),
                                        'Open searcher menu', self)
            clustering_action.triggered.connect(lambda checked,
                                               current_album=album:
                                        self.searcher_menu(current_album))
            searcher_btn = QToolButton(self)
            searcher_btn.setDefaultAction(clustering_action)

            if not album.is_clustered:
                clustering_action.setVisible(False)

            line_number += SHIFT
            self.grid.addWidget(edit_menu_btn, line_number, 0, 1, 1)
            self.grid.addWidget(searcher_btn, line_number, 1, 1, 1)
            self.grid.addWidget(album_label, line_number, 2, 1, 1)

    def searcher_menu(self, album):
        self.search_menu = SearchingMenuWidget(album, self.SCREEN_WIDTH,
                                               self.SCREEN_HEIGHT)
        self.search_menu.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.search_menu.exec_()

    def open_edit_menu(self, album):
        self.menu = EditAlbumWidget(album, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.menu.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.menu.name_changed.nameChanged.connect(self.change_album_name)
        self.menu.clustering_happened.albumClustered.connect(self.redraw)
        self.menu.album_deleted.albumDeleted.connect(self.delete_album)
        self.menu.exec_()

    def change_album_name(self, old, new):
        index = -1
        i = -1
        for album in self.albums:
            if album.album_name == new:
                return
            i += 1
            if album.album_name == old:
                index = i
        self.albums[index].rename_album(new)
        self.menu.setWindowTitle(new + ' menu')
        self.redraw()

    def delete_album(self, album_name):
        for album in self.albums:
            if album_name == album.album_name:
                self.albums.remove(album)
                break
        self.redraw()


class AlbumWidget(QWidget):
    def __init__(self, parent, width, height):
        super(AlbumWidget, self).__init__(parent)
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.__init_UI()

    def __init_UI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        create_album_button = QPushButton('Create album', self)
        self.grid.addWidget(create_album_button, 0, 1, 1, 1)

        self.explorer = AlbumNavigateWidget(self, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        create_album_button.clicked.connect(self.explorer.create_album)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.explorer)

        self.grid.addWidget(scroll_area, 1, 1, 10, 10)

        self.show()

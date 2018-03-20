from PyQt5.QtCore import pyqtSignal, QObject


class ChangeMode(QObject):
    modeChanged = pyqtSignal(bool)


class ChangeDirectory(QObject):
    directoryChanged = pyqtSignal(str)


class AlbumNameChanged(QObject):
    nameChanged = pyqtSignal(str, str)


class AlbumDeleted(QObject):
    albumDeleted = pyqtSignal(str)


class DataSaved(QObject):
    dataSaved = pyqtSignal()


class AlbumClustered(QObject):
    albumClustered = pyqtSignal()

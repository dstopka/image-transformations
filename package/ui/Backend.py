from PySide2.QtCore import QObject, Signal, Property


class Backend(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)



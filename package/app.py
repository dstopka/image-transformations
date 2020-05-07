import sys
from os.path import abspath, dirname, join

from PySide2.QtCore import QObject, Slot
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

def run():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Get the path of the current directory, and then add the name
    # of the QML file, to load it.
    qml_file = join(dirname(__file__), 'views/main.qml')
    engine.load(abspath(qml_file))

    if not engine.rootObjects():
        sys.exit(-1)

    return app.exec_()

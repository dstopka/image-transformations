import sys
from os.path import abspath, dirname, join
from PySide2.QtCore import QObject, Slot
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from .ui.backend import Backend


def run():
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    backend = Backend()
    backend.deviation_changed.connect(lambda deviation: print(deviation))
    backend.mask_size_changed.connect(lambda mask_size: print(mask_size))
    backend.length_changed.connect(lambda length: print(length))
    backend.angle_changed.connect(lambda angle: print(angle))
    engine.rootContext().setContextProperty("backend", backend)
    qml_file = join(dirname(__file__), 'views/main.qml')
    engine.load(abspath(qml_file))

    if not engine.rootObjects():
        sys.exit(-1)

    return app.exec_()

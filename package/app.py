import sys
from os.path import abspath, dirname, join
from PySide2.QtCore import QObject, Slot
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from .ui.backend import *


def run():
    sys.argv += ['--style', 'material']
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    backend = Backend()
    # backend.parameters.deviationChanged.connect(lambda deviation: print(deviation))
    # backend.parameters.maskSizeChanged.connect(lambda mask_size: print(mask_size))
    # backend.parameters.lengthChanged.connect(lambda length: print(length))
    # backend.parameters.angleChanged.connect(lambda angle: print(angle))
    engine.rootContext().setContextProperty("backend", backend)
    engine.rootContext().setContextProperty("parameters", backend.parameters)
    engine.addImageProvider("imgprovider", backend.image_provider)
    qml_file = join(dirname(__file__), 'views/main.qml')
    engine.load(abspath(qml_file))

    if not engine.rootObjects():
        sys.exit(-1)

    return app.exec_()

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtQml import *
from PySide2.QtQuick import *
import cv2


class ImageProvider(QQuickImageProvider):
    def __init__(self):
        super().__init__(QQuickImageProvider.Image)
        self._output_image = None

    def requestImage(self, id:str, size:QSize, requestedSize:QSize) -> QImage:
        print("request")
        return self._output_image


class Backend(QObject):
    deviationChanged = Signal(float)
    maskSizeChanged = Signal(float)
    lengthChanged = Signal(float)
    angleChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._deviation = 0
        self._maskSize = 0
        self._length = 0
        self._angle = 0
        self._input_image = []
        self._output_image = []
        self._image_provider = ImageProvider()

    @Property(str, notify=deviationChanged)
    def deviation(self):
        return self._deviation

    @deviation.setter
    def deviation(self, deviation):
        if self._deviation == float(deviation):
            return
        self._deviation = float(deviation)
        self.deviationChanged.emit(self._deviation)

    @Property(str, notify=maskSizeChanged)
    def maskSize(self):
        return self._maskSize

    @maskSize.setter
    def maskSize(self, mask_size):
        if self._maskSize == float(mask_size):
            return
        self._maskSize = float(mask_size)
        self.maskSizeChanged.emit(self._maskSize)

    @Property(str, notify=lengthChanged)
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        if self._length == float(length):
            return
        self._length = float(length)
        self.lengthChanged.emit(self._length)

    @Property(str, notify=angleChanged)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        if self._angle == float(angle):
            return
        self._angle = float(angle)
        self.angleChanged.emit(self._angle)

    @Slot(str)
    def load_image(self, url):
        print(url)
        self._input_image = cv2.imread(url[7:])
        x, y = self._input_image.shape[:2]
        self._image_provider._output_image = self.make_qimage(self._input_image)
        print(x)

    @staticmethod
    def make_qimage(image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return q_img

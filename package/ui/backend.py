from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtQml import *
from PySide2.QtQuick import *
import numpy as np
import cv2


class Backend(QObject):
    dataReady = Signal(str, name='dataReady')

    def __init__(self, parent=None):
        super().__init__(parent)
        self._input_image = None
        self._output_image = None
        self.parameters = Parameters()
        self.image_provider = ImageProvider()

    @Slot(str)
    def load_image(self, url):
        print(url)
        self._input_image = cv2.imread(url[7:])
        x, y = self._input_image.shape[:2]
        self.image_provider._output_image = self.make_qimage(self._input_image)

    @Slot(int)
    def transform_image(self, opt):
        if opt == 3:
            self.convex_surrounding()

    def convex_surrounding(self):
        self.dataReady.emit("image://imgprovider/data.jpg")

    @staticmethod
    def make_qimage(img: np.ndarray) -> QImage:
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        return q_img


class Image:
    def __init__(self):
        self._img = None


class Parameters(QObject):
    deviationChanged = Signal(float)
    maskSizeChanged = Signal(float)
    lengthChanged = Signal(float)
    angleChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._deviation = None
        self._maskSize = None
        self._length = None
        self._angle = None

    @Property(str, notify=deviationChanged)
    def deviation(self):
        return self._deviation

    @deviation.setter
    def set_deviation(self, deviation):
        if self._deviation == float(deviation):
            return
        self._deviation = float(deviation)
        self.deviationChanged.emit(self._deviation)

    @Property(str, notify=maskSizeChanged)
    def mask_size(self):
        return self._maskSize

    @mask_size.setter
    def set_mask_size(self, mask_size):
        if self._maskSize == float(mask_size):
            return
        self._maskSize = float(mask_size)
        self.maskSizeChanged.emit(self._maskSize)

    @Property(str, notify=lengthChanged)
    def length(self):
        return self._length

    @length.setter
    def set_length(self, length):
        if self._length == float(length):
            return
        self._length = float(length)
        self.lengthChanged.emit(self._length)

    @Property(str, notify=angleChanged)
    def angle(self):
        return self._angle

    @angle.setter
    def set_angle(self, angle):
        if self._angle == float(angle):
            return
        self._angle = float(angle)
        self.angleChanged.emit(self._angle)


class ImageProvider(QQuickImageProvider):
    def __init__(self):
        super().__init__(QQuickImageProvider.Image)
        self._output_image = None

    def requestImage(self, id: str, size: QSize, requestedSize: QSize) -> QImage:
        print("request")
        return self._output_image

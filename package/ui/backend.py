from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtQml import *
from PySide2.QtQuick import *
import numpy as np
import cv2
import random
from package.transformations.imtrans import *
import matplotlib.pyplot as plt


class Backend(QObject):
    outputReady = Signal(str, name='outputReady')
    warning = Signal(str, name='warning')

    def __init__(self, parent=None):
        super().__init__(parent)
        self._input_img = None
        self._output_img = None
        self.parameters = Parameters()
        self.image_provider = ImageProvider()
        self._count = 0

    @Slot(str)
    def load_image(self, url):
        self._input_img = cv2.imread(url[7:], cv2.IMREAD_UNCHANGED)
        self._output_img = None
        self.outputReady.emit("")

    @Slot(str)
    def save_image(self, url):
        if self._output_img is None:
            self.warning.emit("Cannot save non-existing output image! To save please make transformation.")
            return
        cv2.imwrite(url[7:], self._output_img)

    @Slot(int)
    def transform_image(self, opt):
        if self._input_img is None:
            self.warning.emit("Before transforming, an input image must be loaded!")
            return
        self.outputReady.emit("")
        if opt == 0:
            self._output_img = histogram_matching(self._input_img, self.parameters.deviation)
            self.image_provider.make_qimage(self._output_img)
        elif opt == 1:
            self._output_img = entropy_filter(self._input_img, self.parameters.mask_size)
        elif opt == 2:
            self._output_img = imopen(self._input_img, self.parameters.length, self.parameters.angle)
        elif opt == 3:
            self._output_img = convex_hull(self._input_img)
        self._count += 1
        self.image_provider.make_qimage(self._output_img)
        self.outputReady.emit("image://imgprovider/output" + str(self._count))


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
        if self._maskSize == int(mask_size):
            return
        self._maskSize = int(mask_size)
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
        self._image = None

    def requestImage(self, id: str, size: QSize, requestedSize: QSize) -> QImage:
        return self._image

    def make_qimage(self, img) -> QImage:
        height, width = img.shape[:2]
        if image_type(img) == 'BGR':
            bytes_per_line = 3 * width
            self._image = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        else:
            self._image = QImage(img.data, width, height, width, QImage.Format_Grayscale8)

    @property
    def img(self):
        return self._image

    @img.setter
    def img(self, img):
        if self._image != img:
            self._image = img

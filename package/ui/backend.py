from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtQml import *
from PySide2.QtQuick import *
import numpy as np
import cv2
from package.transformations.imtrans import ImageTransform
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

    @Slot(str)
    def load_image(self, url):
        self._input_img = cv2.imread(url[7:], cv2.IMREAD_UNCHANGED)
        #self._input_img = cv2.cvtColor(self._input_img, cv2.COLOR_BGR2RGB)
        self._output_img = None

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
        if opt == 0:
            #self._output_img = ImageTransform.gauss_hist(self._input_img)
            self._output_img = self._input_img
        elif opt == 1:
            self._output_img = ImageTransform.filt_entropy(self._input_img)
        elif opt == 2:
            self._output_img = ImageTransform.imopen(self._input_img)
        elif opt == 3:
            self._output_img = ImageTransform.convex_surr(self._input_img)
        #self._output_img = self._input_img
        plt.subplot(1, 2, 1), plt.imshow(self._input_img, cmap='gray', vmin=0, vmax=255)
        plt.subplot(1, 2, 2), plt.imshow(self._output_img, cmap='gray', vmin=0, vmax=255)
        plt.show()  # To show figure
        #self.image_provider.make_qimage(self._output_img)
        #self.outputReady.emit("image://imgprovider/data.jpg")


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
        self._image = None

    def requestImage(self, id: str, size: QSize, requestedSize: QSize) -> QImage:
        return self._image

    def make_qimage(self, img) -> QImage:
        height, width = img.shape
        bytes_per_line = 3 * width
        self._image = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

    @property
    def img(self):
        return self._image

    @img.setter
    def img(self, img):
        if self._image != img:
            self._image = img

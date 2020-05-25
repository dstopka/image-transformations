from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtQuick import *
import cv2
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

    @Slot()
    def show_histograms(self):
        pass

    @Slot(int)
    def transform_image(self, opt):
        if self._input_img is None:
            self.warning.emit("Before transforming, an input image must be loaded!")
            return
        self.outputReady.emit("")
        if opt == 0:
            self._output_img = histogram_matching(self._input_img, self.parameters.deviation)
        elif opt == 1:
            self._output_img = entropy_filter(self._input_img, self.parameters.mask_size)
        elif opt == 2:
            self._output_img = imopen(self._input_img, self.parameters.length, self.parameters.angle)
        elif opt == 3:
            self._output_img = convex_hull(self._input_img)

        self._count += 1
        self.image_provider.make_qimage(self._output_img)
        self.outputReady.emit("image://imgprovider/output" + str(self._count))

    @Slot()
    def show_histograms(self):
        if self._input_img is None:
            self.warning.emit("No image to show histogram!")
            return
        elif self._output_img is None:
            input_type = image_type(self._input_img)
            if input_type == 'BGR':
                hist_blue = calculate_histogram(self._input_img[:, :, 0])
                hist_green = calculate_histogram(self._input_img[:, :, 1])
                hist_red = calculate_histogram(self._input_img[:, :, 2])
                plt.subplot(131), plt.title("Red"), plt.bar(range(256), hist_red)
                plt.subplot(132), plt.title("Green"), plt.bar(range(256), hist_green)
                plt.subplot(133), plt.title("Blue"), plt.bar(range(256), hist_blue)
            else:
                hist = calculate_histogram(self._input_img)
                plt.title("Mono"), plt.bar(range(256), hist)
        else:
            input_type = image_type(self._input_img)
            output_type = image_type(self._output_img)
            if input_type != 'BGR' and output_type != 'BGR':
                hist_input = calculate_histogram(self._input_img)
                plt.subplot(121), plt.title("Input Mono"), plt.bar(range(256), hist_input)
                hist_output = calculate_histogram(self._output_img)
                plt.subplot(122), plt.title("Output Mono"), plt.bar(range(256), hist_output)
            else:
                if input_type == 'BGR':
                    hist_blue = calculate_histogram(self._input_img[:, :, 0])
                    hist_green = calculate_histogram(self._input_img[:, :, 1])
                    hist_red = calculate_histogram(self._input_img[:, :, 2])
                    plt.subplot(231), plt.title("Input Red"), plt.bar(range(256), hist_red)
                    plt.subplot(232), plt.title("Input Green"), plt.bar(range(256), hist_green)
                    plt.subplot(233), plt.title("Input Blue"), plt.bar(range(256), hist_blue)
                else:
                    hist = calculate_histogram(self._input_img)
                    plt.subplot(231), plt.title("Input Mono"), plt.bar(range(256), hist)
                if output_type == 'BGR':
                    hist_blue = calculate_histogram(self._output_img[:, :, 0])
                    hist_green = calculate_histogram(self._output_img[:, :, 1])
                    hist_red = calculate_histogram(self._output_img[:, :, 2])
                    plt.subplot(234), plt.title("Output Red"), plt.bar(range(256), hist_red)
                    plt.subplot(235), plt.title("Output Green"), plt.bar(range(256), hist_green)
                    plt.subplot(236), plt.title("Output Blue"), plt.bar(range(256), hist_blue)
                else:
                    hist = calculate_histogram(self._output_img)
                    plt.subplot(234), plt.title("Output Mono"), plt.bar(range(256), hist)

        plt.show()


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

from PySide2.QtCore import QObject, Signal, Property, Slot
import cv2


class Backend(QObject):
    deviation_changed = Signal(float)
    mask_size_changed = Signal(float)
    length_changed = Signal(float)
    angle_changed = Signal(float)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._deviation = 0
        self._mask_size = 0
        self._length = 0
        self._angle = 0
        self._input_image = []

    @Property(str, notify=deviation_changed)
    def deviation(self):
        return self._deviation

    @deviation.setter
    def set_deviation(self, deviation):
        if self._deviation == float(deviation):
            return
        self._deviation = float(deviation)
        self.deviation_changed.emit(self._deviation)

    @Property(str, notify=mask_size_changed)
    def mask_size(self):
        return self._mask_size

    @mask_size.setter
    def set_mask_size(self, mask_size):
        if self._mask_size == float(mask_size):
            return
        self._mask_size = float(mask_size)
        self.mask_size_changed.emit(self._mask_size)

    @Property(str, notify=length_changed)
    def length(self):
        return self._length

    @length.setter
    def set_length(self, length):
        if self._length == float(length):
            return
        self._length = float(length)
        self.length_changed.emit(self._length)

    @Property(str, notify=angle_changed)
    def angle(self):
        return self._angle

    @angle.setter
    def set_angle(self, angle):
        if self._angle == float(angle):
            return
        self._angle = float(angle)
        self.angle_changed.emit(self._angle)

    @Slot(str)
    def load_image(self, url):
        print(url)
        self._input_image = cv2.imread(url[7:])
        x, y = self._input_image.shape[:2]
        print(x)

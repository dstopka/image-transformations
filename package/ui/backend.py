from PySide2.QtCore import QObject, Signal, Property


class Backend(QObject):
    deviation_changed = Signal(float)
    mask_size_changed = Signal(float)
    #deviationChanged = Signal(float)
    #deviationChanged = Signal(float)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._deviation = 0
        self._mask_size = 0

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

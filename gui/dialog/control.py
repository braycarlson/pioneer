from __future__ import annotations

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QSlider,
    QVBoxLayout,
    QWidget
)


class FloatSlider(QWidget):
    float_changed = pyqtSignal(float)

    def __init__(
        self,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        parent: QWidget | None = None
    ):
        super().__init__(parent)

        self.slider = QSlider(orientation)
        self.slider.valueChanged.connect(self.on_value_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        self.setLayout(layout)

        self._minimum = 0.0
        self._maximum = 1.0
        self._step = 0.01

        self.update_range()

    @property
    def valueChanged(self) -> float:
        return self.slider.valueChanged

    def on_value_changed(self, value: float) -> None:
        float_value = self._minimum + (value * self._step)
        self.float_changed.emit(float_value)

    def setMinimum(self, value: float) -> None:
        self._minimum = value
        self.update_range()

    def setMaximum(self, value: float) -> None:
        self._maximum = value
        self.update_range()

    def setSingleStep(self, value: float) -> None:
        self._step = value
        self.update_range()

    def setValue(self, value: float) -> None:
        internal = int((value - self._minimum) / self._step)
        self.slider.setValue(internal)

    def value(self) -> float:
        return self._minimum + (self.slider.value() * self._step)

    def update_range(self) -> None:
        minimum = int(self._minimum / self._step)
        maximum = int(self._maximum / self._step)

        self.slider.setRange(minimum, maximum)
        self.slider.setSingleStep(1)


class OddSlider(QWidget):
    value_changed = pyqtSignal(int)

    def __init__(
        self,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        parent: QWidget | None = None
    ):
        super().__init__(parent)

        self.slider = QSlider(orientation)
        self.slider.valueChanged.connect(self.on_value_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        self.setLayout(layout)

        self._minimum = 1
        self._maximum = 99

        self.update_range()

    def on_value_changed(self, value: int) -> None:
        if value % 2 == 0:
            self.slider.blockSignals(True)

            value = (
                value + 1
                if value < self._maximum
                else value - 1
            )

            self.slider.setValue(value)
            self.slider.blockSignals(False)

        self.value_changed.emit(value)

    def setMinimum(self, value: int) -> None:
        if value % 2 == 0:
            value = value + 1

        self._minimum = value
        self.update_range()

    def setMaximum(self, value: int) -> None:
        if value % 2 == 0:
            value = value - 1

        self._maximum = value
        self.update_range()

    def setValue(self, value: int) -> None:
        if value % 2 == 0:
            value = value + 1

        self.slider.setValue(value)

    def value(self) -> int:
        return self.slider.value()

    def update_range(self) -> None:
        minimum = (
            self._minimum
            if self._minimum % 2 != 0
            else self._minimum + 1
        )

        maximum = (
            self._maximum
            if self._maximum % 2 != 0
            else self._maximum - 1
        )

        self.slider.setRange(minimum, maximum)
        self.slider.setSingleStep(2)

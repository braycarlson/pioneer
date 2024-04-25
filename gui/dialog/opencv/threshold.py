from __future__ import annotations

from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import ThresholdWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVThreshold(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'threshold'

        self.setWindowTitle('OpenCV: Threshold')

        self.create()
        self.setup()

    def create(self) -> None:
        callback = [self.push]
        self.threshold_widget = ThresholdWidget(callback)

        self.layout.addWidget(self.threshold_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'method': self.threshold_widget.threshold_type_combobox.currentText(),
                'argument': self.threshold_widget.threshold_type_combobox.currentData(),
                'threshold': self.threshold_widget.threshold_slider.value(),
                'block_size': self.threshold_widget.block_size_spinbox.value(),
                'c': self.threshold_widget.c_spinbox.value()
            },
            'signal': 'opencv_threshold'
        }

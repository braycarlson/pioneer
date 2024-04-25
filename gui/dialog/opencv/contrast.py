from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import FloatSliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVContrast(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'contrast'

        self.setWindowTitle('OpenCV: Contrast')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Contrast',
                'current': 1.0
            },
            'slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 1.0,
                'maximum': 3.0,
                'current': 1.0,
                'callback': [self.push]
            }
        }

        self.contrast_widget = FloatSliderWidget(metadata)

        self.layout.addWidget(self.contrast_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'amount': self.contrast_widget.slider.value()
            },
            'signal': 'opencv_contrast'
        }

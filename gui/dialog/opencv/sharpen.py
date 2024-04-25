from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVSharpen(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'sharpen'

        self.setWindowTitle('OpenCV: Sharpen')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Sharpen',
                'current': 0
            },
            'slider': {
                'control': ControlType.SLIDER,
                'minimum': 0,
                'maximum': 100,
                'current': 0,
                'callback': [self.push]
            }
        }

        self.sharpen_widget = SliderWidget(metadata)

        self.layout.addWidget(self.sharpen_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'amount': self.sharpen_widget.slider.value()
            },
            'signal': 'opencv_sharpen'
        }

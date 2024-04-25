from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVCanny(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'canny'

        self.setWindowTitle('OpenCV: Canny Edge Detection')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Lower Threshold',
                'current': 1
            },
            'lower_threshold_slider': {
                'control': ControlType.SLIDER,
                'minimum': 0,
                'maximum': 255,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.lower_threshold_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Upper Threshold',
                'current': 10
            },
            'upper_threshold_slider': {
                'control': ControlType.SLIDER,
                'minimum': 0,
                'maximum': 255,
                'current': 10,
                'callback': [self.push]
            }
        }

        self.upper_threshold_widget = SliderWidget(metadata)

        self.layout.addWidget(self.lower_threshold_widget)
        self.layout.addWidget(self.upper_threshold_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'lower_threshold': self.lower_threshold_widget.slider.value(),
                'upper_threshold': self.upper_threshold_widget.slider.value()
            },
            'signal': 'opencv_canny'
        }

from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVORB(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'orb'

        self.setWindowTitle('OpenCV: ORB')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Features',
                'current': 0
            },
            'slider': {
                'control': ControlType.SLIDER,
                'minimum': 0,
                'maximum': 500,
                'current': 0,
                'callback': [self.push]
            }
        }

        self.features_widget = SliderWidget(metadata)

        self.layout.addWidget(self.features_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'max_features': self.features_widget.slider.value()
            },
            'signal': 'opencv_orb'
        }

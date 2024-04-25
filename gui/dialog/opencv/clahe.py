from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVCLAHE(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'clahe'

        self.setWindowTitle('OpenCV: CLAHE')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Clip Limit',
                'current': 0
            },
            'slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 10,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.clip_limit_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Grid Size',
                'current': 0
            },
            'slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 10,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.grid_size_widget = SliderWidget(metadata)

        self.layout.addWidget(self.clip_limit_widget)
        self.layout.addWidget(self.grid_size_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'clip_limit': self.clip_limit_widget.slider.value(),
                'grid_size': self.grid_size_widget.slider.value()
            },
            'signal': 'opencv_clahe'
        }

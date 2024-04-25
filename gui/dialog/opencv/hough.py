from __future__ import annotations

import numpy as np

from gui.dialog.factory import ControlType
from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVHough(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'hough'

        self.setWindowTitle('OpenCV: Hough Transform')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Rho',
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

        self.rho_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Theta',
                'current': 0
            },
            'slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 180,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.theta_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Threshold',
                'current': 0
            },
            'slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 500,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.threshold_widget = SliderWidget(metadata)

        self.layout.addWidget(self.rho_widget)
        self.layout.addWidget(self.theta_widget)
        self.layout.addWidget(self.threshold_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': 'opencv',
            'name': self.name,
            'parameter': {
                'rho': self.rho_widget.slider.value(),
                'theta': self.theta_widget.slider.value() * np.pi / 180,
                'threshold': self.threshold_widget.slider.value()
            },
            'signal': 'opencv_hough_transform'
        }

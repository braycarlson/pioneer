from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVBilateral(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'bilateral'

        self.setWindowTitle('OpenCV: Bilateral Filter')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Diameter',
                'current': 1
            },
            'slider_d': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 20,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.diameter_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Color Sigma',
                'current': 1
            },
            'slider_sigma_color': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 200,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.sigma_color_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Space Sigma',
                'current': 1
            },
            'slider_sigma_space': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 200,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.sigma_space_widget = SliderWidget(metadata)

        self.layout.addWidget(self.diameter_widget)
        self.layout.addWidget(self.sigma_color_widget)
        self.layout.addWidget(self.sigma_space_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'diameter': self.diameter_widget.slider.value(),
                'sigma_color': self.sigma_color_widget.slider.value(),
                'sigma_space': self.sigma_space_widget.slider.value()
            },
            'signal': 'opencv_bilateral'
        }

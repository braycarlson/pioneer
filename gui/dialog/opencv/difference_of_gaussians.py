from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import FloatSliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVDifferenceOfGaussians(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'difference_of_gaussians'

        self.setWindowTitle('OpenCV: Difference of Gaussians')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Sigma 1',
                'current': 0.2
            },
            'sigma1_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.2,
                'maximum': 10.0,
                'current': 0.2,
                'callback': [self.push]
            }
        }

        self.sigma1_widget = FloatSliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Sigma 2',
                'current': 0.1
            },
            'sigma2_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.1,
                'maximum': 10.0,
                'current': 0.1,
                'callback': [self.push]
            }
        }

        self.sigma2_widget = FloatSliderWidget(metadata)

        self.layout.addWidget(self.sigma1_widget)
        self.layout.addWidget(self.sigma2_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'sigma1': self.sigma1_widget.slider.value(),
                'sigma2': self.sigma2_widget.slider.value()
            },
            'signal': 'opencv_difference_of_gaussians'
        }

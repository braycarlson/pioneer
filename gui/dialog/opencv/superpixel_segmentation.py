from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVSuperpixelSegmentation(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'superpixel_segmentation'

        self.setWindowTitle('OpenCV: Superpixel Segmentation')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Number of Superpixels',
                'current': 1
            },
            'num_superpixels_slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 1000,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.num_superpixels_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Compactness',
                'current': 10
            },
            'compactness_slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 100,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.compactness_widget = SliderWidget(metadata)

        self.layout.addWidget(self.num_superpixels_widget)
        self.layout.addWidget(self.compactness_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'num_superpixels': self.num_superpixels_widget.slider.value(),
                'compactness': self.compactness_widget.slider.value()
            },
            'signal': 'opencv_superpixel_segmentation'
        }

from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import FloatSliderWidget, SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitSuperpixelSegmentation(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'superpixel_segmentation'

        self.setWindowTitle('Scikit: Superpixel Segmentation')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Number of Segments',
                'current': 1
            },
            'n_segments_slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 500,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.n_segments_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Compactness',
                'current': 0.1
            },
            'compactness_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.1,
                'maximum': 30.0,
                'current': 0.1,
                'callback': [self.push]
            }
        }

        self.compactness_widget = FloatSliderWidget(metadata)

        self.layout.addWidget(self.n_segments_widget)
        self.layout.addWidget(self.compactness_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'n_segments': self.n_segments_widget.slider.value(),
                'compactness': self.compactness_widget.slider.value(),
            },
            'signal': 'scikit_superpixel_segmentation'
        }

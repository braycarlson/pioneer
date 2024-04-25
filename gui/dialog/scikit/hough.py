from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitHough(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'hough'

        self.setWindowTitle('Scikit: Hough Transform')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Threshold',
                'current': 1
            },
            'threshold_slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 100,
                'current': 10,
                'callback': [self.push]
            }
        }

        self.threshold_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Line Length',
                'current': 1
            },
            'line_length_slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 50,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.line_length_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Line Gap',
                'current': 1
            },
            'line_gap_slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 20,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.line_gap_widget = SliderWidget(metadata)

        self.layout.addWidget(self.threshold_widget)
        self.layout.addWidget(self.line_length_widget)
        self.layout.addWidget(self.line_gap_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'threshold': self.threshold_widget.slider.value(),
                'line_length': self.line_length_widget.slider.value(),
                'line_gap': self.line_gap_widget.slider.value(),
            },
            'signal': 'scikit_hough_transform'
        }

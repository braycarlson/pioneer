from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import FloatSliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitCanny(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'canny'

        self.setWindowTitle('Scikit: Canny Edge Detection')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Sigma',
                'current': 1.0
            },
            'sigma_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.1,
                'maximum': 3.0,
                'current': 1.0,
                'callback': [self.push]
            }
        }

        self.sigma_widget = FloatSliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Low Threshold',
            },
            'low_threshold_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.0,
                'maximum': 1.0,
                'current': 0.1,
                'callback': [self.push]
            }
        }

        self.low_threshold_widget = FloatSliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'High Threshold',
            },
            'high_threshold_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.0,
                'maximum': 1.0,
                'current': 0.2,
                'callback': [self.push]
            }
        }

        self.high_threshold_widget = FloatSliderWidget(metadata)

        self.layout.addWidget(self.sigma_widget)
        self.layout.addWidget(self.low_threshold_widget)
        self.layout.addWidget(self.high_threshold_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'sigma': self.sigma_widget.slider.value(),
                'low_threshold': self.low_threshold_widget.slider.value(),
                'high_threshold': self.high_threshold_widget.slider.value(),
            },
            'signal': 'scikit_canny'
        }

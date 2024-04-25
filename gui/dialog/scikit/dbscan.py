from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import FloatSliderWidget, SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitDBSCAN(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'dbscan'

        self.setWindowTitle('Scikit: DBSCAN')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Epsilon',
                'current': 0.0
            },
            'slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.0,
                'maximum': 10.0,
                'current': 0.0,
                'callback': [self.push]
            }
        }

        self.epsilon_widget = FloatSliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Min Samples',
                'current': 0
            },
            'slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 100,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.min_samples_widget = SliderWidget(metadata)

        self.layout.addWidget(self.epsilon_widget)
        self.layout.addWidget(self.min_samples_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'eps': self.epsilon_widget.slider.value(),
                'min_samples': self.min_samples_widget.slider.value()
            },
            'signal': 'scikit_dbscan'
        }

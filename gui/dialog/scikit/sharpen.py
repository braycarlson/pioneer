from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import FloatSliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitSharpen(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'sharpen'

        self.setWindowTitle('Scikit: Sharpen')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Alpha',
                'current': 0.0
            },
            'alpha_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.0,
                'maximum': 3.0,
                'current': 0.0,
                'callback': [self.push]
            }
        }

        self.alpha_widget = FloatSliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Amount',
                'current': 0.0
            },
            'amount_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.0,
                'maximum': 3.0,
                'current': 0.0,
                'callback': [self.push]
            }
        }

        self.amount_widget = FloatSliderWidget(metadata)

        self.layout.addWidget(self.alpha_widget)
        self.layout.addWidget(self.amount_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'alpha': self.alpha_widget.slider.value(),
                'amount': self.amount_widget.slider.value(),
            },
            'signal': 'scikit_sharpen'
        }

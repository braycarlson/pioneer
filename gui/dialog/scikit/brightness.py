from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import FloatSliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitBrightness(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'brightness'

        self.setWindowTitle('Scikit: Brightness')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Gamma',
                'current': 0.0
            },
            'gamma_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.1,
                'maximum': 3.0,
                'current': 0.0,
                'callback': [self.push]
            },
        }

        self.gamma_widget = FloatSliderWidget(metadata)

        self.layout.addWidget(self.gamma_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'gamma': self.gamma_widget.slider.value(),
            },
            'signal': 'scikit_brightness'
        }

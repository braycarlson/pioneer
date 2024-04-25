from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import FloatSliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitContrast(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'contrast'

        self.setWindowTitle('Scikit: Contrast')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Contrast',
                'current': 0.1
            },
            'contrast_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.1,
                'maximum': 2.0,
                'current': 0.1,
                'callback': [self.push]
            },
        }

        self.contrast_widget = FloatSliderWidget(metadata)

        self.layout.addWidget(self.contrast_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'contrast': self.contrast_widget.slider.value(),
            },
            'signal': 'scikit_contrast'
        }

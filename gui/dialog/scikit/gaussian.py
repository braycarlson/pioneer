from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import FloatSliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitGaussian(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'gaussian'

        self.setWindowTitle('Scikit: Gaussian Blur')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Sigma',
                'current': 0.0
            },
            'sigma_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.0,
                'maximum': 5.0,
                'current': 0.0,
                'callback': [self.push]
            },
        }

        self.sigma_widget = FloatSliderWidget(metadata)

        self.layout.addWidget(self.sigma_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'sigma': self.sigma_widget.slider.value(),
            },
            'signal': 'scikit_gaussian_blur'
        }

from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import FloatSliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitBilateral(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'bilateral'

        self.setWindowTitle('Scikit: Bilateral Filter')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Sigma Color',
                'current': 1.0
            },
            'sigma_color_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.1,
                'maximum': 3.0,
                'current': 1.0,
                'callback': [self.push]
            }
        }

        self.sigma_color_widget = FloatSliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Sigma Spatial',
            },
            'sigma_spatial_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.1,
                'maximum': 3.0,
                'current': 1.0,
                'callback': [self.push]
            }
        }

        self.sigma_spatial_widget = FloatSliderWidget(metadata)

        self.layout.addWidget(self.sigma_color_widget)
        self.layout.addWidget(self.sigma_spatial_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'sigma_color': self.sigma_color_widget.slider.value(),
                'sigma_spatial': self.sigma_spatial_widget.slider.value(),
            },
            'signal': 'scikit_bilateral'
        }

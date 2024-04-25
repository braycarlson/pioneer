from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import FloatSliderWidget, SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitCLAHE(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'clahe'

        self.setWindowTitle('Scikit: CLAHE')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Clip Limit',
                'current': 0.01
            },
            'clip_limit_slider': {
                'control': ControlType.FLOAT_SLIDER,
                'minimum': 0.01,
                'maximum': 0.1,
                'current': 0.01,
                'callback': [self.push]
            }
        }

        self.clip_limit_widget = FloatSliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Grid Size',
                'current': 4
            },
            'grid_size_slider': {
                'control': ControlType.SLIDER,
                'minimum': 4,
                'maximum': 16,
                'current': 4,
                'callback': [self.push]
            }
        }

        self.grid_size_widget = SliderWidget(metadata)

        self.layout.addWidget(self.clip_limit_widget)
        self.layout.addWidget(self.grid_size_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'clip_limit': self.clip_limit_widget.slider.value(),
                'grid_size': self.grid_size_widget.slider.value(),
            },
            'signal': 'scikit_clahe'
        }

from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitHOG(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'hog'

        self.setWindowTitle('Scikit: HOG')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Orientation',
                'current': 0
            },
            'slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 18,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.orientation_widget = SliderWidget(metadata)

        self.layout.addWidget(self.orientation_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'orientation': self.orientation_widget.slider.value()
            },
            'signal': 'scikit_hog'
        }

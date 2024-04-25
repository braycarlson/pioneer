from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import ComboboxWidget, KernelWidget, SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitThreshold(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'threshold'

        self.setWindowTitle('Scikit: Threshold')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Method',
            },
            'method_combobox': {
                'control': ControlType.COMBOBOX,
                'items': [
                    ('Otsu', 'otsu'),
                    ('Local', 'local'),
                ],
                'callback': [self.on_method_change]
            }
        }

        self.method_widget = ComboboxWidget(metadata)

        callback = [self.push]
        self.block_size_widget = KernelWidget(callback)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Offset',
                'current': 0
            },
            'offset_slider': {
                'control': ControlType.SLIDER,
                'minimum': -50,
                'maximum': 50,
                'current': 0,
                'callback': [self.push]
            }
        }

        self.offset_widget = SliderWidget(metadata)

        self.layout.addWidget(self.method_widget)
        self.layout.addWidget(self.block_size_widget)
        self.layout.addWidget(self.offset_widget)

    def on_method_change(self) -> None:
        method = self.method_widget.combobox.currentData()
        self.block_size_widget.setDisabled(method != 'local')
        self.offset_widget.setDisabled(method != 'local')

    def send(self) -> dict[str, Any]:
        method = self.method_widget.combobox.currentData()

        if method == 'otsu':
            parameter = {'method': 'otsu'}
        else:
            parameter = {
                'method': 'local',
                'block_size': self.block_size_widget.slider.value(),
                'offset': self.offset_widget.slider.value(),
            }

        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': parameter,
            'signal': 'scikit_threshold'
        }

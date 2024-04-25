from __future__ import annotations

import cv2

from gui.dialog.factory import ControlType
from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import ComboboxWidget, SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVScharrOperator(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'scharr'

        self.setWindowTitle('OpenCV: Scharr Operator')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Derivative Order (dx)',
                'current': 1
            },
            'dx_slider': {
                'control': ControlType.SLIDER,
                'minimum': 0,
                'maximum': 2,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.dx_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Derivative Order (dy)',
                'current': 0
            },
            'dy_slider': {
                'control': ControlType.SLIDER,
                'minimum': 0,
                'maximum': 2,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.dy_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Scale',
                'current': 1
            },
            'scale_slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 100,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.scale_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Delta',
                'current': 0
            },
            'delta_slider': {
                'control': ControlType.SLIDER,
                'minimum': 0,
                'maximum': 100,
                'current': 0,
                'callback': [self.push]
            }
        }

        self.delta_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Border Type',
            },
            'border_type_combobox': {
                'control': ControlType.COMBOBOX,
                'items': [
                    ('Default', cv2.BORDER_DEFAULT),
                    ('Constant', cv2.BORDER_CONSTANT),
                    ('Reflect', cv2.BORDER_REFLECT),
                    ('Reflect 101', cv2.BORDER_REFLECT101),
                    ('Replicate', cv2.BORDER_REPLICATE)
                ],
                'callback': [self.push]
            }
        }

        self.border_type_widget = ComboboxWidget(metadata)

        self.layout.addWidget(self.dx_widget)
        self.layout.addWidget(self.dy_widget)
        self.layout.addWidget(self.scale_widget)
        self.layout.addWidget(self.delta_widget)
        self.layout.addWidget(self.border_type_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'dx': self.dx_widget.slider.value(),
                'dy': self.dy_widget.slider.value(),
                'scale': self.scale_widget.slider.value() / 100.0,
                'delta': self.delta_widget.slider.value(),
                'border_type': self.border_type_widget.combobox.currentData()
            },
            'signal': 'opencv_scharr'
        }

from __future__ import annotations

import cv2

from gui.dialog.factory import ControlType
from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import ComboboxWidget, KernelWidget, SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVSobel(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'sobel'

        self.setWindowTitle('OpenCV: Sobel Edge Detection')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Destination Depth'
            },
            'destination_depth_combobox': {
                'control': ControlType.COMBOBOX,
                'items': [
                    ('8U', cv2.CV_8U),
                    ('16U', cv2.CV_16U),
                    ('64F', cv2.CV_64F)
                ],
                'callback': [self.push]
            }
        }

        self.destination_depth_widget = ComboboxWidget(metadata)

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

        callback = [self.push]
        self.kernel_size_widget = KernelWidget(callback)

        self.layout.addWidget(self.destination_depth_widget)
        self.layout.addWidget(self.dx_widget)
        self.layout.addWidget(self.dy_widget)
        self.layout.addWidget(self.kernel_size_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'destination_depth': self.destination_depth_widget.combobox.currentData(),
                'dx': self.dx_widget.slider.value(),
                'dy': self.dy_widget.slider.value(),
                'kernel_size': self.kernel_size_widget.slider.value()
            },
            'signal': 'opencv_sobel'
        }

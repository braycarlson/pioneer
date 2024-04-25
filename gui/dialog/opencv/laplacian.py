from __future__ import annotations

import cv2

from gui.dialog.factory import ControlType
from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import ComboboxWidget, KernelWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVLaplacian(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'laplacian'

        self.setWindowTitle('OpenCV: Laplacian Edge Detection')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Destination Depth',
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

        callback = [self.push]
        self.kernel_size_widget = KernelWidget(callback)

        self.layout.addWidget(self.destination_depth_widget)
        self.layout.addWidget(self.kernel_size_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'destination_depth': self.destination_depth_widget.combobox.currentData(),
                'kernel_size': self.kernel_size_widget.slider.value()
            },
            'signal': 'opencv_laplacian'
        }

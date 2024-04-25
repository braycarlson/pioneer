from __future__ import annotations

from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import KernelWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVGaussian(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'gaussian'

        self.setWindowTitle('OpenCV: Gaussian Blur')

        self.create()
        self.setup()

    def create(self) -> None:
        callback = [self.push]
        self.gaussian_widget = KernelWidget(callback)

        self.layout.addWidget(self.gaussian_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'kernel_size': self.gaussian_widget.slider.value()
            },
            'signal': 'opencv_gaussian'
        }

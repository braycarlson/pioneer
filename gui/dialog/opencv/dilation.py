from __future__ import annotations

from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import IterationWidget, KernelWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVDilation(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'dilation'

        self.setWindowTitle('OpenCV: Dilation')

        self.create()
        self.setup()

    def create(self) -> None:
        callback = [self.push]
        self.dilation_widget = KernelWidget(callback)
        self.iteration_widget = IterationWidget(callback)

        self.layout.addWidget(self.dilation_widget)
        self.layout.addWidget(self.iteration_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'kernel_size': self.dilation_widget.slider.value(),
                'iterations': self.iteration_widget.slider.value()
            },
            'signal': 'opencv_dilation'
        }

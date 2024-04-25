from __future__ import annotations

from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import KernelWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitMedian(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'median'

        self.setWindowTitle('Scikit: Median Blur')

        self.create()
        self.setup()

    def create(self) -> None:
        callback = [self.push]
        self.kernel_size_widget = KernelWidget(callback)

        self.layout.addWidget(self.kernel_size_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'kernel_size': self.kernel_size_widget.slider.value(),
            },
            'signal': 'scikit_median_blur'
        }

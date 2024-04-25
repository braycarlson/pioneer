from __future__ import annotations

from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import IterationWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitTopHat(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'top_hat'

        self.setWindowTitle('Scikit: Top Hat')

        self.create()
        self.setup()

    def create(self) -> None:
        callback = [self.push]
        self.iteration_widget = IterationWidget(callback)

        self.layout.addWidget(self.iteration_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'iterations': self.iteration_widget.slider.value(),
            },
            'signal': 'scikit_top_hat'
        }

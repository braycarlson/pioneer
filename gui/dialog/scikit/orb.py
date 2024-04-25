from __future__ import annotations

from gui.dialog.scikit.dialog import ScikitDialog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitORB(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'orb'

        self.setWindowTitle('Scikit: ORB')

        self.create()
        self.setup()

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {},
            'signal': 'scikit_orb'
        }

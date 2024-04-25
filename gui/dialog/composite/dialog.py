from __future__ import annotations

from gui.dialog.floating import Dialog


class CompositeDialog(Dialog):
    def __init__(self):
        super().__init__()
        self.library = 'composite'

from __future__ import annotations

from functools import partial
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QWidget


class PILMenu(QMenu):
    def __init__(self, parent: QWidget | None = None):
        super().__init__('&PIL', parent)

        callback = partial(parent.on_preview, 'pil_brightness')
        brightness = QAction('Brightness', self)
        brightness.triggered.connect(callback)

        callback = partial(parent.on_preview, 'pil_contrast')
        contrast = QAction('Contrast', self)
        contrast.triggered.connect(callback)

        self.addAction(brightness)
        self.addAction(contrast)

from __future__ import annotations

from functools import partial
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QWidget


class CompositeMenu(QMenu):
    def __init__(self, parent: QWidget | None = None):
        super().__init__('&Composite', parent)

        callback = partial(parent.on_preview, 'composite_segmentation')
        segmentation = QAction('Segmentation', self)
        segmentation.triggered.connect(callback)

        self.addAction(segmentation)

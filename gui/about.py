from __future__ import annotations

from gui.dialog.floating import Floating
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt6.QtGui import QCloseEvent


class About(Floating):
    terminate = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('About')
        self.setFixedSize(250, 100)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        author = QLabel('Brayden Carlson')
        license = QLabel('GPL v3')
        copyright = QLabel('Copyright © 2024')

        self.layout.addWidget(author)
        self.layout.addWidget(license)
        self.layout.addWidget(copyright)

        self.setLayout(self.layout)

    def closeEvent(self, _: QCloseEvent) -> None:
        self.terminate.emit()

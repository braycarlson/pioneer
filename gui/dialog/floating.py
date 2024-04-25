from __future__ import annotations

from abc import abstractmethod
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QCloseEvent, QGuiApplication, QIcon
from PyQt6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class Floating(QWidget):
    def __init__(self):
        super().__init__()

        self.icon = QIcon('asset/avs.png')
        self.setWindowIcon(self.icon)

    def geometry(self) -> None:
        screen = (
            QGuiApplication
            .primaryScreen()
            .availableGeometry()
        )

        self.screen_width = screen.width()
        self.screen_height = screen.height()

        self.window_width = self.width()
        self.window_height = self.height()

        self.wt = (self.screen_width - self.window_width) / 2
        self.ht = (self.screen_height - self.window_height) / 2
        self.wb = self.window_width
        self.hb = self.window_height

        self.setGeometry(
            int(self.wt),
            int(self.ht),
            int(self.wb),
            int(self.hb)
        )

class Dialog(Floating):
    apply = pyqtSignal(dict)
    cancel = pyqtSignal(dict)
    preview = pyqtSignal(dict)
    terminate = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setFixedWidth(350)
        self.layout = QVBoxLayout(self)

    def setup(self) -> None:
        group = QHBoxLayout()

        self.apply_button = QPushButton('Apply', self)
        self.apply_button.clicked.connect(self.on_apply)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.on_cancel)

        group.addWidget(self.apply_button)
        group.addWidget(self.cancel_button)

        self.layout.addStretch(1)
        self.adjustSize()
        self.layout.addSpacing(40)
        self.layout.addLayout(group)

    def on_apply(self) -> None:
        data = self.send()
        self.apply.emit(data)

        self.close()

    def on_cancel(self) -> None:
        self.close()

    def push(self) -> dict[str, Any]:
        data = self.send()
        self.preview.emit(data)

    @abstractmethod
    def send(self) -> dict[str, Any]:
        raise NotImplementedError

    def closeEvent(self, event: QCloseEvent) -> None:
        data = self.send()
        self.terminate.emit(data)

        event.accept()

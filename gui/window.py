from __future__ import annotations

from functools import partial
from gui.document import Document, DocumentComponentFactory
from gui.menu.main import Menu
from gui.tab import TabWidget
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog
)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('pioneer')
        self.move(100, 100)
        self.resize(1920, 1080)

        # Tab widget
        self.factory = DocumentComponentFactory()
        self.tab = TabWidget(self)
        self.setCentralWidget(self.tab)

        # Menu
        self.menu = Menu()
        self.setMenuBar(self.menu)

        # Connection(s)
        self.menu.browse.connect(self.on_click_load)
        self.menu.save.connect(self.on_click_save)
        self.menu.exit.connect(QApplication.quit)

        callback = partial(self.forward, 'on_filter_preview')
        self.menu.dialog_filter_preview.connect(callback)

        callback = partial(self.forward, 'on_filter_applied')
        self.menu.dialog_filter_applied.connect(callback)

        callback = partial(self.forward, 'on_filter_canceled')
        self.menu.dialog_filter_canceled.connect(callback)

    def forward(
        self,
        signal: str,
        data: dict[str: float | str] | None = None
    ) -> None:
        if data is None:
            data = {}

        tab = self.tab.currentWidget()

        if not tab:
            return

        if data is not None:
            getattr(tab.panel, signal)(data)

    def on_click_load(self) -> None:
        directory = 'E:/code/personal/thesis/dataset/mnist/training/0/1.png'

        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open file',
            filter='Image (*.jpg *.jpeg *.png)',
            directory=directory
        )

        if not path:
            QMessageBox.warning(
                self,
                'Warning',
                'Please provide a valid path.'
            )

            return

        document = Document(self.factory, path)
        document.create()

        self.tab.create(document)

    def on_click_save(self) -> None:
        pass

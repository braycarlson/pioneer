from __future__ import annotations

from gui.dialog.manager import DialogManager
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QTabWidget,
    QWidget,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.document import Document
    from gui.scroll import ScrollableWindow


class TabWidget(QTabWidget):
    tab_changed = pyqtSignal(int)

    def __init__(
        self,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.manager = DialogManager()
        self.stack = []

        self.setTabsClosable(True)
        self.currentChanged.connect(self.on_change_tab)
        self.tabCloseRequested.connect(self.on_close_tab)

    @property
    def artboard(self) -> ScrollableWindow:
        if not self.stack:
            return None

        index = self.currentIndex()
        return self.stack[index].artboard

    @property
    def document(self) -> Document:
        if not self.stack:
            return None

        index = self.currentIndex()
        return self.stack[index]

    @property
    def identifier(self) -> str:
        if not self.stack:
            return None

        index = self.currentIndex()
        return self.stack[index].identifier

    def create(self, document: Document) -> None:
        self.stack.append(document)
        self.addTab(document, document.path)
        self.setCurrentIndex(self.count() - 1)

    def on_change_tab(self) -> None:
        self.tab_changed.emit(self.identifier)

    def on_close_tab(self, index: int) -> None:
        if self.identifier is not None:
            self.manager.reset(self.identifier)

        del self.stack[index]
        self.removeTab(index)

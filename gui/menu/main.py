from __future__ import annotations

import uuid

from gui.about import About
from gui.dialog.manager import DialogManager
from gui.menu.composite import CompositeMenu
from gui.menu.opencv import OpenCVMenu
from gui.menu.pillow import PILMenu
from gui.menu.scikit import ScikitMenu
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar


class Menu(QMenuBar):
    # File
    browse = pyqtSignal()
    save = pyqtSignal()
    exit = pyqtSignal()

    # Options
    settings = pyqtSignal()
    preferences = pyqtSignal()

    # Dialog
    dialog_filter_preview = pyqtSignal(dict)
    dialog_filter_applied = pyqtSignal(dict)
    dialog_filter_canceled = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.manager = DialogManager()

        # File
        file = self.addMenu('&File')

        browse = QAction('Browse', parent=self)
        browse.triggered.connect(self.on_click_browse)

        exit = QAction('Exit', parent=self)
        exit.triggered.connect(self.on_click_exit)

        save = QAction('Save', parent=self)
        save.triggered.connect(self.on_click_save)

        file.addAction(browse)
        file.addAction(save)
        file.addAction(exit)

        # Composite
        self.composite = CompositeMenu(self)
        self.addMenu(self.composite)

        # OpenCV
        self.opencv = OpenCVMenu(self)
        self.addMenu(self.opencv)

        # PIL
        self.pil = PILMenu(self)
        self.addMenu(self.pil)

        # Scikit-Image
        self.scikit = ScikitMenu(self)
        self.addMenu(self.scikit)

        # Options
        options = self.addMenu('&Options')

        settings = QAction('Settings', parent=self)
        settings.triggered.connect(self.on_click_settings)

        options.addAction(settings)

        # Help
        help = self.addMenu("&Help")

        self.about = None
        self.current = None

        about = QAction('About', parent=self)
        about.triggered.connect(self.on_click_about)

        help.addAction(about)

    def on_preview(self, signal: str) -> None:
        if self.current is not None:
            self.current.activateWindow()
        else:
            tid = self.parent().tab.identifier

            unique = uuid.uuid4()
            fid = str(unique)

            self.current = self.manager.get(tid, signal, fid)
            self.current.preview.connect(self.dialog_filter_preview.emit)
            self.current.apply.connect(self.dialog_filter_applied.emit)
            self.current.cancel.connect(self.dialog_filter_canceled.emit)
            self.current.cancel.connect(self.on_exit_current)
            self.current.terminate.connect(self.dialog_filter_canceled.emit)
            self.current.terminate.connect(self.on_exit_current)

            self.current.geometry()
            self.current.show()

    def on_click_about(self) -> None:
        if self.about is not None:
            self.about.activateWindow()
        else:
            self.about = About()
            self.about.terminate.connect(self.on_exit_about)

            self.about.geometry()
            self.about.show()

    def on_click_browse(self) -> None:
        self.browse.emit()

    def on_click_exit(self) -> None:
        self.exit.emit()

    def on_click_save(self) -> None:
        self.save.emit()

    def on_click_settings(self) -> None:
        self.settings.emit()

    def on_exit_about(self) -> None:
        if self.about is not None:
            self.about.deleteLater()

        self.about = None

    def on_exit_current(self) -> None:
        if self.current is not None:
            self.current.close()
            self.current = None

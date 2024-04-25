from __future__ import annotations

import cv2
import uuid

from gui.panel import FilterPanel
from gui.scroll import ScrollableWindow
from gui.state import ImageState
from matplotlib.figure import Figure
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy.typing as npt

    from matplotlib.axes import Axes
    from PyQt6.QtWidgets import QTabWidget


class DocumentComponentFactory:
    def create_canvas(self) -> tuple[Axes, Figure]:
        fig = Figure()
        ax = fig.add_subplot(111, autoscale_on=True)

        return (ax, fig)

    def create_scrollable_window(
        self,
        ax: Axes,
        fig: Figure,
        image: npt.NDArray
    ) -> ScrollableWindow:
        window = ScrollableWindow(ax, fig)
        window.update(image)
        return window

    def create_image_state(self, image: npt.NDArray) -> ImageState:
        return ImageState(image)

    def create_filter_panel(
        self,
        parent: QTabWidget,
        state: ImageState
    ) -> FilterPanel:
        return FilterPanel(parent, state)


class Document(QWidget):
    def __init__(self, factory: DocumentComponentFactory, path: str):
        super().__init__()

        self.factory = factory
        self.layout = QHBoxLayout(self)
        self.path = path

    def create(self) -> None:
        unique = uuid.uuid4()
        self.identifier = str(unique)

        image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)

        self.fig, self.ax = self.factory.create_canvas()
        self.artboard = self.factory.create_scrollable_window(self.ax, self.fig, image)
        self.state = self.factory.create_image_state(image)
        self.panel = self.factory.create_filter_panel(self, self.state)

        group = self.panel.create_button_group()

        left = QVBoxLayout()
        right = QVBoxLayout()

        left.addWidget(self.artboard)
        right.addWidget(self.panel)
        right.addWidget(group)

        self.layout.addLayout(left, 3)
        self.layout.addLayout(right, 1)

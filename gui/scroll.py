from __future__ import annotations

from gui.canvas import Canvas
from matplotlib.backend_bases import MouseButton
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QScrollArea,
    QWidget
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy.typing as npt

    from matplotlib.axes import Axes
    from matplotlib.backend_bases import MouseEvent
    from matplotlib.figure import Figure


class ScrollableWindow(QWidget):
    def __init__(self, fig: Figure, ax: Axes):
        super().__init__()

        self.minimum = 1.0
        self.last = None
        self.zoom = 1.0

        self.canvas = Canvas(fig, ax)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)

        self.scroll = QScrollArea(self)
        self.scroll.resizeEvent = self.on_resize
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.canvas)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)

        self.setFixedWidth(1280)

    @property
    def maximum(self) -> float:
        length = self.canvas.x_maximum - self.canvas.x_minimum
        width = self.canvas.width()

        if length == 0:
            return float('inf')

        maximum = width / length

        restriction = 2 ** 16
        image = restriction / width
        return min(maximum, image)

    def on_motion(self, event: MouseEvent) -> None:
        if hasattr(self, 'press') and self.press:
            x, _ = self.press

            if self.x is not None:
                dx = event.x - x
                self.x = event.x

                scroll = self.scroll.horizontalScrollBar().value()

                factor = 0.5
                scroll = scroll - int(dx * factor)

                self.scroll.horizontalScrollBar().setValue(scroll)
            else:
                self.x = event.x

    def on_press(self, event: MouseEvent) -> None:
        if event.button == MouseButton.RIGHT:
            self.press = event.x, event.y

    def on_release(self, event: MouseEvent) -> None:
        if event.button == MouseButton.RIGHT:
            self.press = None

    def on_resize(self, event: MouseEvent) -> None:
        viewport = self.scroll.viewport().size()
        scroll = event.size().width()

        width = int(scroll * self.zoom)
        height = int(viewport.height() * (width / viewport.width()))

        self.canvas.setFixedWidth(width)
        self.canvas.setFixedHeight(height)

    def on_scroll(self, event: MouseEvent) -> None:
        if event.button == 'up':
            if self.zoom >= self.maximum:
                return

            self.zoom = min(self.zoom * 1.50, self.maximum)

        if event.button == 'down':
            if self.zoom <= self.minimum:
                return

            self.zoom = max(self.zoom * 0.50, self.minimum)

        size = self.scroll.viewport().size()
        resize = QResizeEvent(size, size)

        # Calculate the center of the current viewport
        center_x = self.scroll.viewport().width() / 2
        center_y = self.scroll.viewport().height() / 2

        # Apply zoom and redraw
        self.on_resize(resize)
        self.canvas.draw_idle()

        # Calculate new scroll positions based on the center
        sx = int(center_x * self.zoom - center_x)
        sy = int(center_y * self.zoom - center_y)

        # Ensure the scroll positions are within the allowed range
        sx = min(max(0, sx), self.scroll.horizontalScrollBar().maximum())
        sy = min(max(0, sy), self.scroll.verticalScrollBar().maximum())

        # Update the scroll positions
        self.scroll.horizontalScrollBar().setValue(sx)
        self.scroll.verticalScrollBar().setValue(sy)

    def update(self, image: npt.NDArray) -> None:
        self.canvas.ax.clear()

        self.canvas.image = self.canvas.ax.matshow(
            image,
            aspect='auto',
            cmap='gray',
            interpolation=None,
            origin='upper'
        )

        self.canvas.ax.set_axis_off()
        self.canvas.draw_idle()

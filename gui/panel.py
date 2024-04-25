from __future__ import annotations

from constant import ACTION
from functools import partial
from gui.dialog.manager import DialogManager
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QWidget
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor, QIcon, QPainter, QPaintEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.state import ImageState
    from typing_extensions import Any


class FilterItem(QListWidgetItem):
    def __init__(self, data: dict[str, Any]):
        super().__init__()

        self.identifier = data.get('identifier')
        self.library = data.get('library')
        self.name = data.get('name').lower()
        self.parameter = data.get('parameter')
        self.is_visible = True
        self.display = self.name.title()
        self.signal = data.get('signal')


class FilterWidget(QWidget):
    visibility_changed = pyqtSignal(FilterItem)
    parameter_changed = pyqtSignal(FilterItem)

    def __init__(self, item: FilterItem):
        super().__init__()

        self.item = item

        self.layout = QHBoxLayout(self)
        self.create_button_group()

    def create_button_group(self) -> QWidget:
        path = ACTION.joinpath('visibility_on.png').as_posix()
        icon = QIcon(path)

        self.visibility_button = QPushButton()
        self.visibility_button.setIcon(icon)
        self.visibility_button.clicked.connect(self.on_toggle_visibility)
        self.visibility_button.setFlat(True)
        self.visibility_button.setFixedWidth(20)

        self.update_visibility_icon()

        path = ACTION.joinpath('edit.png').as_posix()
        icon = QIcon(path)

        self.edit_button = QPushButton()
        self.edit_button.setIcon(icon)
        self.edit_button.clicked.connect(self.on_edit_filter)
        self.edit_button.setFlat(True)
        self.edit_button.setFixedWidth(20)

        self.label = QLabel(self.item.display)

        self.layout.addWidget(self.visibility_button)
        self.layout.addWidget(self.edit_button)
        self.layout.addWidget(self.label)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.setSpacing(10)

        self.setLayout(self.layout)

    def on_toggle_visibility(self) -> None:
        self.update_visibility_icon()
        self.visibility_changed.emit(self.item)

    def update_visibility_icon(self) -> None:
        if self.item.is_visible:
            path = ACTION.joinpath('visibility_on.png').as_posix()
        else:
            path = ACTION.joinpath('visibility_off.png').as_posix()

        icon = QIcon(path)
        self.visibility_button.setIcon(icon)

    def on_edit_filter(self) -> None:
        self.parameter_changed.emit(self.item)


class FilterPanel(QListWidget):
    visibility_changed = pyqtSignal(FilterItem)
    parameter_changed = pyqtSignal(FilterItem)

    def __init__(
        self,
        parent: QWidget | None = None,
        state: ImageState = None
    ):
        super().__init__(parent)

        self.current = None
        self.manager = DialogManager()
        self.dialog = None
        self.state = state

        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.visibility_changed.connect(self.on_visibility_change)
        self.parameter_changed.connect(self.on_parameter_change)
        self.state.refresh.connect(self.update_ui)

    def create_button_group(self) -> QWidget:
        group = QWidget()
        layout = QHBoxLayout()

        path = ACTION.joinpath('add.png').as_posix()
        icon = QIcon(path)
        add = QPushButton(icon, '')

        path = ACTION.joinpath('arrow_up.png').as_posix()
        icon = QIcon(path)
        up = QPushButton(icon, '')

        path = ACTION.joinpath('arrow_down.png').as_posix()
        icon = QIcon(path)
        down = QPushButton(icon, '')

        path = ACTION.joinpath('delete.png').as_posix()
        icon = QIcon(path)
        delete = QPushButton(icon, '')

        add.clicked.connect(self.on_add_filter)
        up.clicked.connect(self.on_move_up)
        down.clicked.connect(self.on_move_down)
        delete.clicked.connect(self.on_delete_filter)

        layout.addWidget(add)
        layout.addWidget(up)
        layout.addWidget(down)
        layout.addWidget(delete)

        group.setLayout(layout)
        return group

    def emit_visibility(self, item: FilterItem) -> None:
        self.visibility_changed.emit(item)

    def emit_parameter(self, item: FilterItem) -> None:
        self.parameter_changed.emit(item)

    def on_parameter_change(self, item: FilterItem) -> None:
        for method in self.state.filter:
            if method.identifier == item.identifier:
                self.current = item

                tid = self.parent().identifier
                dialog = self.manager.get(tid, item.signal, item.identifier)

                callback = partial(self.on_filter_canceled, None)
                dialog.cancel.connect(callback)

                dialog.show()

                break

    def on_visibility_change(self, item: FilterItem) -> None:
        self.current = item

        self.state.toggle_visibility(item.identifier)
        self.update_ui()

    def on_filter_preview(self, data: dict[str, float | str]) -> None:
        # Get the preview image from ImageState
        image = self.state.preview_filter(data)

        # Update the artboard with the preview image
        if self.parent().artboard is not None:
            self.parent().artboard.update(image)

    def on_filter_applied(self, data: dict[str: float | str]) -> None:
        self.state.add_filter(data)
        self.update_ui()

    def on_filter_canceled(self, data: dict[str: float | str]) -> None:
        signal = data.get('signal')
        fid = data.get('identifier')

        tid = self.parent().identifier
        self.manager.remove(tid, signal, fid)

        self.parent().artboard.update(self.state.image)
        self.update_ui()

    def update_artboard(self) -> None:
        if self.parent().artboard is not None:
            self.parent().artboard.update(self.state.image)

    def update_ui(self) -> None:
        self.clear()

        for item in self.state.filter:
            self._add_filter_widget(item)

        self.update_artboard()

    def update_filter(self, data: dict[str, Any]) -> None:
        self.state.update_filter(data)
        self.update_ui()

    def on_add_filter(self) -> None:
        pass

    def on_move_up(self) -> None:
        row = self.currentRow()

        if row > 0:
            self.state.filter[row], self.state.filter[row - 1] = (
                self.state.filter[row - 1],
                self.state.filter[row]
            )

            self.state.apply_filter()
            self.refresh_list()
            self.setCurrentRow(row - 1)
            self.setFocus()

    def on_move_down(self) -> None:
        row = self.currentRow()

        if row < len(self.state.filter) - 1:
            self.state.filter[row], self.state.filter[row + 1] = (
                self.state.filter[row + 1],
                self.state.filter[row]
            )

            self.state.apply_filter()
            self.refresh_list()
            self.setCurrentRow(row + 1)
            self.setFocus()

    def on_delete_filter(self) -> None:
        row = self.currentRow()

        if row != -1:
            item = self.state.filter[row]

            tid = self.parent().identifier
            self.manager.remove(tid, item.signal, item.identifier)

            del self.state.filter[row]
            self.takeItem(row)

            self.state.remove_filter(item.identifier)

            self.update_ui()

    def add_filter(self, item: FilterItem) -> None:
        # Add the filter to the ImageState's filter list
        self.state.add_filter(item)

        # Refresh the list UI
        self.refresh_list()

        # Select the newly added filter item in the UI
        row = len(self.state.filter) - 1
        index = self.item(row)
        self.setCurrentItem(index)
        self.setFocus()

    def refresh_list(self) -> None:
        self.clear()

        for name in self.state.filter:
            self._add_filter_widget(name)

    def _add_filter_widget(self, item: FilterItem) -> None:
        row = QListWidgetItem(self)

        # Create the widget with the current filter item
        widget = FilterWidget(item)
        widget.visibility_changed.connect(self.emit_visibility)
        widget.parameter_changed.connect(self.emit_parameter)

        # Update the visibility icon to reflect the current state
        widget.update_visibility_icon()

        self.setItemWidget(row, widget)
        hint = widget.sizeHint()
        row.setSizeHint(hint)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        viewport = self.viewport()
        painter = QPainter(viewport)

        count = self.count()

        for index in range(count):
            item = self.item(index)

            if not item.isSelected() and index % 2 == 0:
                rectangle = self.visualItemRect(item)

                color = QColor(68, 68, 68)
                painter.fillRect(rectangle, color)

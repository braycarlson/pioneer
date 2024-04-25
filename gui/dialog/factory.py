from __future__ import annotations

from enum import Enum
from functools import partial
from gui.dialog.control import FloatSlider, OddSlider
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QLabel,
    QSlider,
    QSpinBox,
    QWidget
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ControlType(Enum):
    CHECKBOX = 'checkbox'
    COMBOBOX = 'combobox'
    FLOAT_SLIDER = 'float_slider'
    LABEL = 'label'
    ODD_SLIDER = 'odd_slider'
    SLIDER = 'slider'
    SPINBOX = 'spinbox'


class ControlFactory:
    @staticmethod
    def create_control(
        parameter: dict[str, Any]
    ) -> QWidget:
        control = parameter.get('control')

        match control:
            case ControlType.CHECKBOX:
                return ControlFactory.create_checkbox(parameter)
            case ControlType.COMBOBOX:
                return ControlFactory.create_combobox(parameter)
            case ControlType.FLOAT_SLIDER:
                return ControlFactory.create_float_slider(parameter)
            case ControlType.LABEL:
                return ControlFactory.create_label(parameter)
            case ControlType.ODD_SLIDER:
                return ControlFactory.create_odd_slider(parameter)
            case ControlType.SLIDER:
                return ControlFactory.create_slider(parameter)
            case ControlType.SPINBOX:
                return ControlFactory.create_spinbox(parameter)
            case _:
                return None

    @staticmethod
    def create(
        parameter: dict[str, Any]
    ) -> QWidget:
        widget = []

        for name in parameter:
            metadata = parameter[name]
            control = ControlFactory.create_control(metadata)
            widget.append(control)

        return widget

    @staticmethod
    def create_checkbox(
        parameter: dict[str, Any]
    ) -> QCheckBox:
        checked = parameter.get('default', False)
        text = parameter.get('text', None)

        checkbox = QCheckBox(text)
        checkbox.setChecked(checked)

        function = parameter.get('callback')

        if function is not None:
            for name in function:
                callback = partial(name)
                checkbox.stateChanged.connect(callback)

        return checkbox

    @staticmethod
    def create_combobox(
        parameter: dict[str, Any]
    ) -> QComboBox:
        items = parameter.get('items', [])

        combobox = QComboBox()

        for label, item in items:
            combobox.addItem(label, item)

        function = parameter.get('callback')

        if function is not None:
            for name in function:
                callback = partial(name)
                combobox.currentIndexChanged.connect(callback)

        return combobox

    @staticmethod
    def create_float_slider(
        parameter: dict[str, Any]
    ) -> FloatSlider:
        minimum = parameter.get('minimum', 0.0)
        maximum = parameter.get('maximum', 1.0)
        current = parameter.get('current', 0.0)
        step = parameter.get('step', 0.01)

        slider = FloatSlider()
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(current)
        slider.setSingleStep(step)

        function = parameter.get('callback')

        if function is not None:
            for name in function:
                callback = partial(name)
                slider.float_changed.connect(callback)

        return slider

    @staticmethod
    def create_label(
        parameter: dict[str, Any]
    ) -> QLabel:
        text = parameter.get('text', None)
        current = parameter.get('current')

        label = QLabel(text)

        if current is None:
            label.setText(text)
        else:
            label.setText(f"{text}: {current}")

        return label

    @staticmethod
    def create_odd_slider(
        parameter: dict[str, Any]
    ) -> FloatSlider:
        minimum = parameter.get('minimum', 1)
        maximum = parameter.get('maximum', 99)
        current = parameter.get('current', 1)

        slider = OddSlider()
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(current)

        function = parameter.get('callback')

        if function is not None:
            for name in function:
                callback = partial(name)
                slider.value_changed.connect(callback)

        return slider

    @staticmethod
    def create_slider(
        parameter: dict[str, Any]
    ) -> QSlider:
        minimum = parameter.get('minimum', 0)
        maximum = parameter.get('maximum', 10)
        current = parameter.get('current', 1)
        step = parameter.get('step', 1)

        slider = QSlider(Qt.Orientation.Horizontal)

        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(current)
        slider.setSingleStep(step)

        function = parameter.get('callback')

        if function is not None:
            for name in function:
                callback = partial(name)
                slider.valueChanged.connect(callback)

        return slider

    @staticmethod
    def create_spinbox(
        parameter: dict[str, Any]
    ) -> QSpinBox:
        minimum = parameter.get('minimum', 0)
        maximum = parameter.get('maximum', 10)
        current = parameter.get('current', 1)
        step = parameter.get('step', 1)

        spinbox = QSpinBox()
        spinbox.setMinimum(minimum)
        spinbox.setMaximum(maximum)
        spinbox.setValue(current)
        spinbox.setSingleStep(step)

        function = parameter.get('callback')

        if function is not None:
            for name in function:
                callback = partial(name)
                spinbox.valueChanged.connect(callback)

        return spinbox

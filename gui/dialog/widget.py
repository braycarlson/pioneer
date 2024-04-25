from __future__ import annotations

import cv2

from gui.dialog.factory import ControlFactory, ControlType
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from typing_extensions import Any


class ComboboxWidget(QWidget):
    def __init__(self, metadata: dict[str, Any]):
        super().__init__()

        self.metadata = metadata

        self.layout = QVBoxLayout(self)

        self.label, self.combobox = ControlFactory.create(metadata)
        self.layout.addWidget(self.label)
        self.layout.addSpacing(3)
        self.layout.addWidget(self.combobox)


class FloatSliderWidget(QWidget):
    def __init__(self, metadata: dict[str, Any]):
        super().__init__()

        self.metadata = metadata

        self.layout = QVBoxLayout(self)
        self.label, self.slider = ControlFactory.create(metadata)
        self.slider.valueChanged.connect(self.on_label_text_change)

        self.layout.addWidget(self.label)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.slider)

    def on_label_text_change(self, amount: float) -> None:
        normalize = amount / 100

        text = self.metadata.get('label').get('text')
        self.label.setText(f"{text}: {normalize:.2f}")


class HorizontalRuleWidget(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)


class KernelWidget(QWidget):
    def __init__(self, callback: list[Callable] | None = None):
        super().__init__()

        self.callback = callback

        self.metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Kernel Size',
                'current': 1
            },
            'slider': {
                'control': ControlType.ODD_SLIDER,
                'minimum': 1,
                'maximum': 99,
                'current': 1,
                'callback': self.callback
            }
        }

        self.layout = QVBoxLayout(self)
        self.label, self.slider = ControlFactory.create(self.metadata)
        self.slider.value_changed.connect(self.on_label_text_change)

        self.layout.addWidget(self.label)
        self.layout.addSpacing(3)
        self.layout.addWidget(self.slider)

        left, _, right, _ = self.layout.getContentsMargins()
        self.layout.setContentsMargins(left, 0, right, 0)

    def on_label_text_change(self, amount: int) -> None:
        text = self.metadata.get('label').get('text')
        self.label.setText(f"{text}: {amount}")


class SimpleKernelWidget(QWidget):
    def __init__(self, metadata: dict[str, Any]):
        super().__init__()

        self.metadata = metadata

        self.layout = QVBoxLayout(self)
        self.label, self.slider = ControlFactory.create(metadata)
        self.slider.value_changed.connect(self.on_label_text_change)

        self.layout.addWidget(self.label)
        self.layout.addSpacing(3)
        self.layout.addWidget(self.slider)

        left, _, right, _ = self.layout.getContentsMargins()
        self.layout.setContentsMargins(left, 0, right, 0)

    def on_label_text_change(self, amount: int) -> None:
        text = self.metadata.get('label').get('text')
        self.label.setText(f"{text}: {amount}")


class SliderWidget(QWidget):
    def __init__(self, metadata: dict[str, Any]):
        super().__init__()

        self.metadata = metadata

        self.layout = QVBoxLayout(self)
        self.label, self.slider = ControlFactory.create(metadata)
        self.slider.valueChanged.connect(self.on_label_text_change)

        self.layout.addWidget(self.label)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.slider)

    def on_label_text_change(self, amount: int) -> None:
        text = self.metadata.get('label').get('text')
        self.label.setText(f"{text}: {amount}")


class SpinboxWidget(QWidget):
    def __init__(self, metadata: dict[str, Any]):
        super().__init__()

        self.metadata = metadata

        self.layout = QVBoxLayout(self)
        self.label, self.spinbox = ControlFactory.create(metadata)

        self.layout.addWidget(self.label)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.spinbox)


class IterationWidget(QWidget):
    def __init__(self, callback: list[Callable] | None = None):
        super().__init__()

        self.callback = callback

        self.metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Iteration(s)',
                'current': 1
            },
            'iterations_slider': {
                'control': ControlType.SLIDER,
                'minimum': 1,
                'maximum': 99,
                'current': 1,
                'callback': self.callback
            },
        }

        self.layout = QVBoxLayout(self)
        self.label, self.slider = ControlFactory.create(self.metadata)
        self.slider.valueChanged.connect(self.on_label_text_change)

        self.layout.addWidget(self.label)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.slider)

    def on_label_text_change(self, amount: int) -> None:
        text = self.metadata.get('label').get('text')
        self.label.setText(f"{text}: {amount}")


class ThresholdWidget(QWidget):
    def __init__(self, callback: list[Callable] | None = None):
        super().__init__()

        self.callback = callback

        self.layout = QVBoxLayout(self)

        self.metadata = {
            'combobox_label': {
                'control': ControlType.LABEL,
                'text': 'Threshold Type'
            },
            'combobox': {
                'control': ControlType.COMBOBOX,
                'items': [
                    ('Binary', cv2.THRESH_BINARY),
                    ('Binary Inverted', cv2.THRESH_BINARY_INV),
                    ('Truncate', cv2.THRESH_TRUNC),
                    ('To Zero', cv2.THRESH_TOZERO),
                    ('To Zero Inverted', cv2.THRESH_TOZERO_INV),
                    ('Otsu\'s Binarization', cv2.THRESH_BINARY + cv2.THRESH_OTSU),
                    ('Adaptive Mean', cv2.THRESH_BINARY_INV),
                    ('Adaptive Gaussian', cv2.THRESH_BINARY_INV)
                ],
                'callback': self.callback
            },
            'slider_label': {
                'control': ControlType.LABEL,
                'text': 'Threshold',
                'current': 0
            },
            'slider': {
                'control': ControlType.SLIDER,
                'minimum': 0,
                'maximum': 255,
                'current': 0,
                'callback': self.callback
            },
            'block_size_label': {
                'control': ControlType.LABEL,
                'text': 'Block Size',
            },
            'block_size_spinbox': {
                'control': ControlType.SPINBOX,
                'minimum': 3,
                'maximum': 255,
                'current': 3,
                'step': 2,
                'callback': self.callback
            },
            'c_label': {
                'control': ControlType.LABEL,
                'text': 'C',
            },
            'c_spinbox': {
                'control': ControlType.SPINBOX,
                'minimum': -255,
                'maximum': 255,
                'current': 1,
                'step': 2,
                'callback': self.callback
            }
        }

        (
            self.threshold_type_combobox_label,
            self.threshold_type_combobox,
            self.threshold_slider_label,
            self.threshold_slider,
            self.block_size_label,
            self.block_size_spinbox,
            self.c_label,
            self.c_spinbox
        ) = ControlFactory.create(self.metadata)

        self.threshold_slider.valueChanged.connect(self.on_label_text_change)
        self.threshold_type_combobox.currentIndexChanged.connect(self.on_threshold_type_change)

        self.threshold_widget = QWidget(self)
        self.threshold_layout = QVBoxLayout(self.threshold_widget)
        self.threshold_layout.setContentsMargins(0, 0, 0, 0)
        self.threshold_layout.addSpacing(10)
        self.threshold_layout.addWidget(self.threshold_slider_label)
        self.threshold_layout.addSpacing(3)
        self.threshold_layout.addWidget(self.threshold_slider)
        self.threshold_layout.addSpacing(5)

        self.adaptive_widget = QWidget(self)
        self.adaptive_layout = QVBoxLayout(self.adaptive_widget)
        self.adaptive_layout.setContentsMargins(0, 0, 0, 0)
        self.adaptive_layout.addSpacing(10)
        self.adaptive_layout.addWidget(self.block_size_label)
        self.threshold_layout.addSpacing(3)
        self.adaptive_layout.addWidget(self.block_size_spinbox)
        self.adaptive_layout.addSpacing(10)
        self.adaptive_layout.addWidget(self.c_label)
        self.threshold_layout.addSpacing(3)
        self.adaptive_layout.addWidget(self.c_spinbox)
        self.adaptive_layout.addSpacing(10)

        self.layout.addWidget(self.threshold_type_combobox_label)
        self.layout.addWidget(self.threshold_type_combobox)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.threshold_widget)
        self.layout.addWidget(self.adaptive_widget)

        left, _, right, _ = self.layout.getContentsMargins()
        self.layout.setContentsMargins(left, 0, right, 0)

        self.threshold_widget.show()
        self.adaptive_widget.hide()

    def on_label_text_change(self, amount: int) -> None:
        self.threshold_slider_label.setText(f"Threshold: {amount}")

    def on_threshold_type_change(self) -> None:
        current = self.threshold_type_combobox.currentText()

        self.threshold_slider.setValue(0)

        if current in ['Adaptive Mean', 'Adaptive Gaussian']:
            self.adaptive_widget.show()
            self.threshold_widget.hide()
        elif current == 'Otsu\'s Binarization':
            self.adaptive_widget.hide()
            self.threshold_widget.hide()
        else:
            self.adaptive_widget.hide()
            self.threshold_widget.show()

        self.parent().adjustSize()

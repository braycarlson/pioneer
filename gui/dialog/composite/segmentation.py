from __future__ import annotations

import cv2

from gui.dialog.factory import ControlType
from gui.dialog.composite.dialog import CompositeDialog
from gui.dialog.widget import (
    ComboboxWidget,
    HorizontalRuleWidget,
    KernelWidget,
    SliderWidget,
    ThresholdWidget
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class CompositeSegmentation(CompositeDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'segmentation'

        self.setWindowTitle('Composite: Segmentation')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Connectivity',
                'current': 0
            },
            'slider': {
                'control': ControlType.SLIDER,
                'minimum': 0,
                'maximum': 8,
                'current': 0,
                'callback': [self.push]
            }
        }

        self.connectivity_widget = SliderWidget(metadata)

        hr1 = HorizontalRuleWidget()

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Distance Type',
            },
            'combobox': {
                'control': ControlType.COMBOBOX,
                'items': [
                    ('DIST_L1', cv2.DIST_L1),
                    ('DIST_L2', cv2.DIST_L2),
                    ('DIST_C', cv2.DIST_C),
                    ('DIST_L12', cv2.DIST_L12),
                    ('DIST_FAIR', cv2.DIST_FAIR),
                    ('DIST_WELSCH', cv2.DIST_WELSCH),
                    ('DIST_HUBER', cv2.DIST_HUBER),
                ],
                'callback': [self.push]
            }
        }

        self.distance_type_widget = ComboboxWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Mask Size',
            },
            'combobox': {
                'control': ControlType.COMBOBOX,
                'items': [
                    ('0', 0),
                    ('3', 3),
                    ('5', 5),
                ],
                'callback': [self.push]
            }
        }

        self.mask_widget = ComboboxWidget(metadata)

        callback = [self.push]
        self.threshold_widget = ThresholdWidget(callback)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Morphology Operation',
            },
            'combobox': {
                'control': ControlType.COMBOBOX,
                'items': [
                    ('Dilation', cv2.MORPH_DILATE),
                    ('Erosion', cv2.MORPH_ERODE)
                ],
                'callback': [self.push]
            }
        }

        self.morphology_widget = ComboboxWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Kernel Size',
                'current': 0
            },
            'slider': {
                'control': ControlType.ODD_SLIDER,
                'minimum': 1,
                'maximum': 21,
                'current': 1,
                'step': 2,
                'callback': [self.push]
            }
        }

        self.kernel_size_widget = KernelWidget(callback)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Distance Transform',
                'current': 0
            },
            'slider': {
                'control': ControlType.SLIDER,
                'minimum': 0,
                'maximum': 255,
                'current': 1,
                'callback': [self.push]
            }
        }

        self.distance_transform_widget = SliderWidget(metadata)

        self.layout.addWidget(self.connectivity_widget)
        self.layout.addWidget(hr1)
        self.layout.addWidget(self.distance_type_widget)
        self.layout.addWidget(self.mask_widget)
        self.layout.addWidget(self.threshold_widget)
        self.layout.addWidget(self.kernel_size_widget)
        self.layout.addWidget(self.distance_transform_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'connectivity': self.connectivity_widget.slider.value(),
                'distance_type': self.distance_type_widget.combobox.currentData(),
                'mask_size': self.mask_widget.combobox.currentData(),
                'morphology_operation': self.morphology_widget.combobox.currentData(),
                'kernel_size': self.kernel_size_widget.slider.value(),
                'threshold_type': self.threshold_widget.threshold_type_combobox.currentData(),
                'threshold': self.threshold_widget.threshold_slider.value(),
                'distance_transform': self.distance_transform_widget.slider.value(),
            },
            'signal': 'composite_segmentation'
        }

from __future__ import annotations

import cv2

from gui.dialog.factory import ControlType
from gui.dialog.opencv.dialog import OpenCVDialog
from gui.dialog.widget import ComboboxWidget, ThresholdWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class OpenCVContour(OpenCVDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'contour'

        self.setWindowTitle('OpenCV: Contour')

        self.create()
        self.setup()

    def create(self) -> None:
        callback = [self.push]
        self.threshold_widget = ThresholdWidget(callback)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Retrieval Mode'
            },
            'combobox': {
                'control': ControlType.COMBOBOX,
                'items': [
                    ('External', cv2.RETR_EXTERNAL),
                    ('List', cv2.RETR_LIST),
                    ('Connected Component', cv2.RETR_CCOMP),
                    ('Tree', cv2.RETR_TREE),
                    # ('Floodfill', cv2.RETR_FLOODFILL),
                ],
                'callback': [self.push]
            }
        }

        self.retrieval_mode_widget = ComboboxWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Approximation Mode'
            },
            'combobox': {
                'control': ControlType.COMBOBOX,
                'items': [
                    ('None', cv2.CHAIN_APPROX_NONE),
                    ('Simple', cv2.CHAIN_APPROX_SIMPLE),
                    ('TC89 L1', cv2.CHAIN_APPROX_TC89_L1),
                    ('TC89 KCOS', cv2.CHAIN_APPROX_TC89_KCOS),
                ],
                'callback': [self.push]
            }
        }

        self.approximation_mode_widget = ComboboxWidget(metadata)

        self.layout.addWidget(self.threshold_widget)
        self.layout.addWidget(self.retrieval_mode_widget)
        self.layout.addWidget(self.approximation_mode_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'threshold_type': self.threshold_widget.threshold_type_combobox.currentData(),
                'threshold': self.threshold_widget.threshold_slider.value(),
                'retrieval_mode': self.retrieval_mode_widget.combobox.currentData(),
                'approximation_mode': self.approximation_mode_widget.combobox.currentData()
            },
            'signal': 'opencv_contour'
        }

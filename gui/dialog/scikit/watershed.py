from __future__ import annotations

from gui.dialog.factory import ControlType
from gui.dialog.scikit.dialog import ScikitDialog
from gui.dialog.widget import ComboboxWidget, SliderWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


class ScikitWatershed(ScikitDialog):
    def __init__(self, identifier: str):
        super().__init__()

        self.identifier = identifier
        self.name = 'watershed'

        self.setWindowTitle('Scikit: Watershed')

        self.create()
        self.setup()

    def create(self) -> None:
        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Marker Type',
            },
            'combobox': {
                'control': ControlType.COMBOBOX,
                'items': [
                    ('Peak Local Max', 'peak_local_max'),
                    ('Random', 'random'),
                    ('Manual', 'manual'),
                    ('Otsu Thresholding', 'otsu_thresholding'),
                    ('Distance Transform', 'distance_transform'),
                ],
                'callback': [self.push]
            }
        }

        self.markers_type_widget = ComboboxWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Markers',
                'current': 0
            },
            'slider': {
                'control': ControlType.SLIDER,
                'minimum': 0,
                'maximum': 100,
                'current': 0,
                'callback': [self.push]
            }
        }

        self.markers_widget = SliderWidget(metadata)

        metadata = {
            'label': {
                'control': ControlType.LABEL,
                'text': 'Connectivity',
                'current': 0
            },
            'slider': {
                'control': ControlType.SLIDER,
                'minimum': 0,
                'maximum': 100,
                'current': 0,
                'callback': [self.push]
            }
        }

        self.connectivity_widget = SliderWidget(metadata)

        self.layout.addWidget(self.markers_type_widget)
        self.layout.addWidget(self.markers_widget)
        self.layout.addWidget(self.connectivity_widget)

    def send(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'library': self.library,
            'name': self.name,
            'parameter': {
                'marker_option': self.markers_type_widget.combobox.currentData(),
                'markers': self.markers_widget.slider.value(),
                'connectivity': self.connectivity_widget.slider.value()
            },
            'signal': 'scikit_watershed'
        }

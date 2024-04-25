from __future__ import annotations

import hashlib
import json

from gui.panel import FilterItem
from filter.factory import FilterFactory
from PyQt6.QtCore import QObject, pyqtSignal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy.typing as npt


class ImageState(QObject):
    refresh = pyqtSignal()

    def __init__(self, original: npt.NDArray = None):
        super().__init__()

        self.cache = {}
        self.mapping = {}
        self.original = original
        self.image = original.copy()
        self.filter = []

    def _apply_and_cache(self) -> None:
        key = self._generate_key(self.filter)

        if key in self.cache:
            self.image = self.cache[key].copy()
        else:
            self.apply_filter()
            self.cache[key] = self.image.copy()

        self.refresh.emit()

    def _generate_key(self, items: list[FilterItem]) -> str:
        # Generate a cache key for the current state including the edited filter
        identifier = [
            (item.identifier, item.is_visible, item.parameter)
            for item in items
        ]

        string = json.dumps(identifier, sort_keys=True).encode()
        return hashlib.md5(string).hexdigest()

    def _update_filter(self, data: dict[str, float | str]) -> list[FilterItem]:
        collection = []

        identifier = data.get('identifier')

        for item in self.filter:
            if item.identifier == identifier:
                is_visible = item.is_visible

                item = FilterItem(data)
                item.is_visible = is_visible

            collection.append(item)

        if not any(item.identifier == identifier for item in self.filter):
            collection.append(FilterItem(data))

        return collection

    def _update_mapping(self, key: str, items: list[FilterItem]) -> None:
        for item in items:
            if item.identifier not in self.mapping:
                self.mapping[item.identifier] = set()

            self.mapping[item.identifier].add(key)

    def apply_filter(self) -> None:
        if self.original is None:
            return

        self.image = self.original.copy()

        for item in self.filter:
            if item.is_visible:
                data = {
                    'identifier': item.identifier,
                    'library': item.library,
                    'name': item.name,
                    'parameter': item.parameter
                }

                instance = FilterFactory.create_filter(data)
                self.image = instance.apply(self.image)

        self.refresh.emit()

    def preview_filter(self, data: dict[str, float | str]) -> npt.NDArray:
        if self.original is None:
            return None

        items = self._update_filter(data)
        key = self._generate_key(items)
        self._update_mapping(key, items)

        if key in self.cache:
            return self.cache[key].copy()

        preview = self.original.copy()

        for item in items:
            if item.is_visible:
                data = {
                    'identifier': item.identifier,
                    'library': item.library,
                    'name': item.name,
                    'parameter': item.parameter
                }

                instance = FilterFactory.create_filter(data)
                preview = instance.apply(preview)

        self.cache[key] = preview.copy()

        return preview

    def add_filter(self, data: dict[str: float | str]) -> None:
        identifier = data.get('identifier')

        item = next(
            (item for item in self.filter if item.identifier == identifier),
            None
        )

        if item:
            item.parameter = data.get('parameter', item.parameter)
        else:
            item = FilterItem(data)
            self.filter.append(item)

        self._apply_and_cache()

    def remove_filter(self, identifier: str) -> None:
        if identifier in self.mapping:
            for key in self.mapping[identifier]:
                if key in self.cache:
                    del self.cache[key]

            del self.mapping[identifier]

        self.filter = [
            item
            for item in self.filter
            if item.identifier != identifier
        ]

        self._apply_and_cache()

    def toggle_visibility(self, identifier: str) -> None:
        for item in self.filter:
            if item.identifier == identifier:
                item.is_visible = not item.is_visible
                break

        self._apply_and_cache()

    def update_filter(self, data: dict[str: float | str]) -> None:
        identifier = data.get('identifier')
        parameter = data.get('parameter')

        for item in self.filter:
            if item.identifier == identifier:
                item.parameter = parameter
                break

        self._apply_and_cache()

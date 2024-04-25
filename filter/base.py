from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy.typing as npt


class BaseFilter:
    def __init__(self, parameter: dict[str, float | int]):
        self.is_visible = True
        self.parameter = parameter

    def apply(self, _: npt.NDArray) -> npt.NDArray:
        message = 'This method should be implemented by subclasses.'
        raise NotImplementedError(message)

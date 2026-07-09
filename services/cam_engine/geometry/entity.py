from __future__ import annotations

from abc import ABC, abstractmethod
from .bbox import BoundingBox

class Entity(ABC):
    """
    Base geometric entity.
    """

    @property
    @abstractmethod
    def start(self):
        ...

    @property
    @abstractmethod
    def end(self):
        ...

    @abstractmethod
    def copy(self):
        ...

    @abstractmethod
    def length(self) -> float:
        ...

    @abstractmethod
    def bbox(self) -> BoundingBox:
        ...

    @abstractmethod
    def translate(self, dx: float, dy: float):
        ...

    @abstractmethod
    def rotate(self, angle_deg: float, origin=None):
        ...

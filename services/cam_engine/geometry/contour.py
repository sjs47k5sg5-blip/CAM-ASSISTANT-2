from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from .entity import Entity
from .bbox import BoundingBox

@dataclass(slots=True)
class Contour:
    entities: list[Entity]=field(default_factory=list)
    closed: bool=True

    def add(self, entity: Entity)->None:
        self.entities.append(entity)

    def extend(self, entities)->None:
        self.entities.extend(entities)

    def copy(self)->"Contour":
        c=Contour(closed=self.closed)
        c.entities=[e.copy() for e in self.entities]
        return c

    @property
    def start(self):
        return self.entities[0].start if self.entities else None

    @property
    def end(self):
        return self.entities[-1].end if self.entities else None

    @property
    def bbox(self)->BoundingBox|None:
        if not self.entities:
            return None
        box=self.entities[0].bbox()
        for e in self.entities[1:]:
            box=box.union(e.bbox())
        return box

    def reverse(self)->"Contour":
        c=Contour(closed=self.closed)
        for e in reversed(self.entities):
            c.add(e.copy())
        return c

    def __len__(self): return len(self.entities)
    def __iter__(self)->Iterator[Entity]: return iter(self.entities)
    def __getitem__(self,index): return self.entities[index]

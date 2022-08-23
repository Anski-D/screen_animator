import pygame as pg
from abc import ABC, abstractmethod


class Movable(ABC):
    def __init__(self):
        self._rect = None

    @property
    def rect(self) -> pg.Rect:
        return self._rect

    @abstractmethod
    def move(self):
        pass


class Item(pg.sprite.Sprite):
    def __init__(
        self, group: pg.sprite.Group, content: pg.Surface, perimeter: pg.Rect
    ) -> None:
        super().__init__(group)
        self.content = content

    @property
    def content(self) -> pg.Surface:
        return self._content

    @content.setter
    def content(self, content: pg.Surface) -> None:
        self._content = content
        self._rect = self._content.get_rect()


class Movement(ABC):
    @abstractmethod
    def move(self, movable: "Movable"):
        pass


class ScrollingMovement(Movement):
    _directions = {
        "up": ("y", -1),
        "right": ("x", 1),
        "down": ("y", 1),
        "left": ("x", -1),
    }

    def __init__(self, speed: int | float = 0, direction: str = "left"):
        self._speed = speed
        self._axis, self._sign = self._set_direction(direction)

    def move(self, movable: Movable) -> None:
        rect = movable.rect
        new_position = getattr(rect, self._axis) + self._sign * self._speed
        setattr(rect, self._axis, new_position)

    def _set_direction(self, direction: str) -> tuple[str, int]:
        return self._directions.get(direction, self._directions["left"])

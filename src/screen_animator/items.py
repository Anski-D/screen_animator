import random

import pygame as pg
from abc import ABC, abstractmethod
import logging

log = logging.getLogger(__name__)


class Movable(ABC):
    def __init__(self):
        self._rect = None
        self._perimeter = None

    @property
    def rect(self) -> pg.Rect:
        return self._rect

    @rect.setter
    def rect(self, rect: pg.Rect):
        self._rect = rect

    @property
    def perimeter(self) -> pg.Rect:
        return self._perimeter

    @perimeter.setter
    def perimeter(self, perimeter: pg.Rect) -> None:
        self._perimeter = perimeter

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
    def move(self, movable: Movable):
        pass


class ScrollingMovement(Movement):
    _directions = {
        "up": ("y", -1),
        "right": ("x", 1),
        "down": ("y", 1),
        "left": ("x", -1),
    }

    def __init__(self, speed: int = 0, direction: str = "left") -> None:
        self._speed = speed
        self.direction = direction

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, speed: int) -> None:
        self._speed = speed

    @property
    def direction(self) -> str:
        return self._direction

    @direction.setter
    def direction(self, direction: str) -> None:
        self._direction = direction
        self._axis, self._sign = self._directions.get(self._direction, self._directions["left"])

    def move(self, movable: Movable) -> None:
        rect = movable.rect
        new_position = getattr(rect, self._axis) + self._sign * self._speed
        setattr(rect, self._axis, new_position)


class RandomMovement(Movement):
    def move(self, movable: Movable):
        movable.rect.left = random.randint(0, movable.perimeter.right - movable.rect.width)
        movable.rect.top = random.randint(0, movable.perimeter.bottom - movable.rect.height)

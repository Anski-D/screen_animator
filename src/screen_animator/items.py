import random
from abc import ABC, abstractmethod
import logging
import pygame as pg

log = logging.getLogger(__name__)


class Movable(ABC):
    """
    An interface for movable items in `pygame`.
    """

    _rect: pg.Rect
    _perimeter: pg.Rect

    @property
    def rect(self) -> pg.Rect:
        """The defining rectangle that can be moved."""
        return self._rect

    @rect.setter
    def rect(self, rect: pg.Rect):
        self._rect = rect

    @property
    def perimeter(self) -> pg.Rect:
        """The outer perimeter of where the movable object is located.

        Movable objects are not required to be within the perimeter, only have a reference to them.
        """
        return self._perimeter

    @perimeter.setter
    def perimeter(self, perimeter: pg.Rect) -> None:
        self._perimeter = perimeter

    @abstractmethod
    def move(self) -> None:
        """Subclasses should implement behaviour to move the instance, typically by manipulating the `rect` property."""


class Item(pg.sprite.Sprite):
    """
    A `pygame` item.
    """
    def __init__(
        self, group: pg.sprite.Group, content: pg.Surface, perimeter: pg.Rect
    ) -> None:
        super().__init__(group)
        self.content = content
        self.perimeter = perimeter

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
        self._axis, self._sign = self._directions.get(
            self._direction, self._directions["left"]
        )

    def move(self, movable: Movable) -> None:
        rect = movable.rect
        new_position = getattr(rect, self._axis) + self._sign * self._speed
        setattr(rect, self._axis, new_position)


class RandomMovement(Movement):
    def move(self, movable: Movable) -> None:
        movable.rect.left = random.randint(
            0, movable.perimeter.right - movable.rect.width
        )
        movable.rect.top = random.randint(
            0, movable.perimeter.bottom - movable.rect.height
        )

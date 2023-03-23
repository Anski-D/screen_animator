import random
from abc import ABC, abstractmethod
import logging

import pygame as pg

log = logging.getLogger(__name__)


class Item(pg.sprite.Sprite):
    """
    A wrapper for `pygame` sprite-type objects that are then can be moved on a `pygame` 'canvas'.

    Attributes
    ----------
    content
        The content of the item.
    rect
        The positioning rectangle of the item.
    perimeter
        The defined outer limits.

    Methods
    -------
    move
        Move as defined by the provided `Movement` type.
    update
        Hook used to execute `move` through a group.
    """

    rect: pg.Rect | pg.rect.Rect

    def __init__(
        self,
        group: pg.sprite.Group,
        content: pg.Surface | pg.surface.Surface,
        perimeter: pg.Rect,
        movement: "Movement" = None,
    ) -> None:
        """Initialise a wrapped `Sprite` that has a group, render-capable content, a defined
        perimeter and a `Movement` type.

        Parameters
        ----------
        group
            The `pygame` group to which to add.
        content
            The `pygame`-type content that can be rendered.
        perimeter
            The outside limits of the `pygame` context, typically the size of the canvas/screen.
        movement : optional
            A method of moving.
        """
        super().__init__(group)

        self.content = content
        self.rect = self.content.get_rect()
        self.perimeter = perimeter
        self._movement = movement

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({super().groups()},"
            f" {self.content},"
            f" {self.perimeter},"
            f" {self._movement})"
        )

    def move(self) -> None:
        """Move the instance using a `Movement` object, if defined."""
        if self._movement is not None:
            self._movement.move(self)

    def update(self, *_args, **_kwargs) -> None:
        """Update the instance (move it)."""
        self.move()


class Movement(ABC):
    """
    A way of moving a `Movable` object.

    Methods
    -------
    move
        Move a `Movable`, to be implemented by sublasses.
    """

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    @abstractmethod
    def move(self, item: Item) -> None:
        """Sublasses should implement a means of moving `Movable`."""


class ScrollingMovement(Movement):
    """
    Define the method of movement as moving at a speed in a direction.

    Methods
    -------
    move
        Move in the direction specified at the set speed.
    """

    _directions = {
        "up": ("y", -1),
        "right": ("x", 1),
        "down": ("y", 1),
        "left": ("x", -1),
    }

    def __init__(self, speed: int = 0, direction: str = "left") -> None:
        """
        Initialise the scrolling style of movement with a set speed and direction.

        Parameters
        ----------
        speed : optional
            The speed of movement in pixels per frame (default is 0).
        direction : optional
            The direction of movement (default is 'left').
        """
        super().__init__()

        self.speed = speed
        self.direction = direction
        log.info("Creating %s", self)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.speed}, {self.direction})"

    @property
    def direction(self) -> str:
        """The direction of movement."""
        return self._direction

    @direction.setter
    def direction(self, direction: str) -> None:
        self._direction = direction
        self._axis, self._sign = self._directions.get(
            self._direction, self._directions["left"]
        )

    def move(self, item: Item) -> None:
        """
        Move input in the direction defined, at the speed set.

        Parameters
        ----------
        item
            Object to move.
        """
        rect = item.rect
        new_position = getattr(rect, self._axis) + self._sign * self.speed
        setattr(rect, self._axis, new_position)


class RandomMovement(Movement):
    """
    Define the method of movement as random within a defined perimeter.

    Methods
    -------
    move
        Move randomly within a perimeter.
    """

    def move(self, item: Item) -> None:
        """
        Move input randomly within a perimeter.

        Parameters
        ----------
        item
            Object to move.
        """
        item.rect.left = random.randint(0, item.perimeter.right - item.rect.width)
        item.rect.top = random.randint(0, item.perimeter.bottom - item.rect.height)

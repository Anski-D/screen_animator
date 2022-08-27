import random
from abc import ABC, abstractmethod
import logging
import pygame as pg

log = logging.getLogger(__name__)


class Movable(pg.sprite.Sprite):
    """
    An interface for movable items in `pygame`.

    Methods
    -------
    move
        Move the instance, to be implemented by sublasses.
    """

    _perimeter: pg.Rect

    @property
    def perimeter(self) -> pg.Rect:
        """
        The outer perimeter of where the movable object is located.

        Movable objects are not required to be within the perimeter, only have a reference to them.
        """
        return self._perimeter

    @perimeter.setter
    def perimeter(self, perimeter: pg.Rect) -> None:
        self._perimeter = perimeter

    @abstractmethod
    def move(self) -> None:
        """Subclasses should implement behaviour to move the instance."""


class Item(Movable):
    """
    A wrapper for `pygame` sprite-type objects that are then can be moved on a `pygame` 'canvas'.

    Methods
    -------
    move
        Move as defined by the provided `Movement` type.
    update
        Hook used to execute `move` through a group.
    """

    def __init__(
        self,
        group: pg.sprite.Group,
        content: pg.Surface,
        perimeter: pg.Rect,
        movement: "Movement" = None,
    ) -> None:
        """Initialise a wrapped `Sprite` that has a group, render-capable content, a defined perimeter and a `Movement` type.

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
        self.perimeter = perimeter
        self._movement = movement

    @property
    def content(self) -> pg.Surface:
        """The `pygame`-type content that can be rendered."""
        return self._content

    @content.setter
    def content(self, content: pg.Surface) -> None:
        self._content = content
        self.rect = self._content.get_rect()

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

    @abstractmethod
    def move(self, movable: Movable):
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
        self._speed = speed
        self.direction = direction

    @property
    def speed(self) -> int:
        """The speed in pixels per frame."""
        return self._speed

    @speed.setter
    def speed(self, speed: int) -> None:
        self._speed = speed

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

    def move(self, movable: Movable) -> None:
        """
        Move input in the direction defined, at the speed set.

        Parameters
        ----------
        movable
            Object to move.
        """
        rect = movable.rect
        new_position = getattr(rect, self._axis) + self._sign * self._speed
        setattr(rect, self._axis, new_position)


class RandomMovement(Movement):
    """
    Define the method of movement as random within a defined perimeter.

    Methods
    -------
    move
        Move randomly within a perimeter.
    """

    def move(self, movable: Movable) -> None:
        """
        Move input randomly within a perimeter.

        Parameters
        ----------
        movable
            Object to move.
        """
        movable.rect.left = random.randint(
            0, movable.perimeter.right - movable.rect.width
        )
        movable.rect.top = random.randint(
            0, movable.perimeter.bottom - movable.rect.height
        )

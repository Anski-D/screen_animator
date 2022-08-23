import pygame as pg
from abc import ABC, abstractmethod


class Item(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, content: pg.Surface, perimeter: pg.Rect):
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
    def move(self, movable: 'Movable'):
        pass


class ScrollingMovement(Movement):
    def __init__(self, speed=0, direction='left'):
        self._speed = speed
        self._direction = direction
        self._axis, self._sign = self._set_direction()

    def move(self, movable: 'Movable'):
        pass

    def _set_direction(self) -> tuple[str, int]:
        match self._direction:
            case 'up':
                return 'y', -1
            case 'right':
                return 'x', 1
            case 'down':
                return 'y', 1
            case _:
                return 'x', -1

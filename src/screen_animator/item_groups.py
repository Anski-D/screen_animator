from abc import ABC, abstractmethod
import pygame as pg
from .items import ScrollingMovement, Item


class ItemGroup(ABC):
    def __init__(self, settings: dict, perimeter: pg.Rect):
        self._settings = settings
        self._perimeter = perimeter
        self._group = pg.sprite.Group()

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def update(self):
        pass


class LeftScrollingText(ItemGroup):
    _movement = ScrollingMovement

    def create(self):
        speed = self._settings["messages"]["scroll_speed"] / self._settings["timings"]["fps"]
        movement = self._movement(speed, "left")
        Item(self._group, self._settings["messages"]["message"](), self._perimeter, movement)

    def update(self):
        pass

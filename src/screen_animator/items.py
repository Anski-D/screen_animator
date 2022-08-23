import pygame as pg


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

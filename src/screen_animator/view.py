import pygame as pg
from .model import Model
from .controller import Controller


class View:
    _screen: pg.Surface
    perimeter: pg.Rect

    def __init__(self, model: Model, controller: Controller, settings: dict) -> None:
        self._model = model
        self._controller = controller
        self._settings = settings
        self._initialized = False

    @property
    def initialized(self) -> bool:
        return self._initialized

    def init(self) -> None:
        self._screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.perimeter = self._screen.get_rect()
        self._set_bg()
        self._initialized = True

    def update(self) -> None:
        self._set_bg()
        for group in self._model.item_groups:
            for item in group.items:
                self._screen.blit(item.content, item.rect)

        pg.display.flip()

    def _set_bg(self) -> None:
        self._screen.fill(self._settings["bg"]["color"])

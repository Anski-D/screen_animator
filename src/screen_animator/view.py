import pygame as pg
from .observers import Observer
from .model import Model


class View(Observer):
    _screen: pg.Surface
    perimeter: pg.Rect

    def __init__(
        self,
        model: Model,
        controller: "Controller",
        settings: dict,
        display_size: tuple[int, int] = None,
        flipped=False,
    ) -> None:
        self._model = model
        self._controller = controller
        self._settings = settings
        self._display_size = display_size
        self._flipped = flipped
        self._initialized = False

    @property
    def initialized(self) -> bool:
        return self._initialized

    def init(self) -> None:
        if self._display_size is None:
            self._screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        else:
            self._screen = pg.display.set_mode(self._display_size)
        pg.display.set_caption("Screen_Animator")
        self.perimeter = self._screen.get_rect()
        self._set_bg()
        self._initialized = True

    def update(self) -> None:
        self._set_bg()
        for group in self._model.item_groups:
            for item in group.items:
                self._screen.blit(item.content, item.rect)

        if self._flipped:
            self._screen.blit(pg.transform.rotate(self._screen, 180), (0, 0))

        pg.display.flip()

    def notify(self) -> None:
        self.update()

    def quit(self) -> None:
        self._initialized = False

    def _set_bg(self) -> None:
        self._screen.fill(self._settings["bg"]["color"])

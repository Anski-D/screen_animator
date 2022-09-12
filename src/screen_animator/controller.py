import pygame as pg
from .model import Model
from .view import View
from .settings import SettingsManager


class Controller:
    def __init__(
        self,
        settings_manager: SettingsManager,
        model: Model,
        display_size: tuple[int, int] = None,
        flipped=False,
    ) -> None:
        self._settings_manager = settings_manager
        self._settings = self._settings_manager.settings
        self._model = model
        self._view = View(model, self, settings_manager.settings, display_size, flipped)
        self._clock = pg.time.Clock()

    @property
    def initialized(self) -> bool:
        return self._view.initialized and self._model.initialized

    def init(self) -> None:
        self._view.init()
        self._model.init(self._view.perimeter)
        self._model.add_observer(self._view)

    def run(self) -> None:
        while self.initialized:
            self._clock.tick(self._settings["timings"]["fps"])
            self._model.update()
            self._check_events()

    def _check_events(self) -> None:
        for event in pg.event.get():
            if is_quit(event):
                for component in [self._view, self._model]:
                    component.quit()


def is_quit(event: pg.event.Event) -> bool:
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
        return True

    return False

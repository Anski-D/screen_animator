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
    ) -> None:
        self._settings_manager = settings_manager
        self._settings = self._settings_manager.settings
        self._model = model
        self._view = View(model, self, settings_manager.settings, display_size)
        self._clock = pg.time.Clock()

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

            pg.event.pump()

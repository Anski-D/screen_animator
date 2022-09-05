import pygame as pg
from .model import Model
from .view import View
from .settings import SettingsManager


class Controller:
    def __init__(self, settings_manager: SettingsManager, model: Model) -> None:
        self._settings_manager = settings_manager
        self._settings = self._settings_manager.settings
        self._model = model
        self._view = View(model, self, settings_manager.settings)
        self._clock = pg.time.Clock()
        self._initialized = False

    def init(self) -> None:
        self._view.init()
        self._model.init(self._view.perimeter)
        self._model.add_observer(self._view)

        if self._view.initialized and self._model.initialized:
            self._initialized = True

    def run(self):
        while self._initialized:
            self._clock.tick(self._settings["timings"]["fps"])

            self._model.update()

            pg.event.pump()

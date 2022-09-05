from .model import Model
from .view import View
from .settings import SettingsManager


class Controller:
    def __init__(self, settings_manager: SettingsManager, model: Model) -> None:
        self._settings_manager = settings_manager
        self._model = model
        self._view = View(model, self, settings_manager.settings)
        self._initialized = False

    def init(self) -> None:
        self._view.init()
        self._model.init(self._view.perimeter)
        self._model.add_observer(self._view)

        if self._view.initialized and self._model.initialized:
            self._initialized = True

from .model import Model
from .view import View


class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self._model = model
        self._view = view

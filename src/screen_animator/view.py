from .model import Model
from .controller import Controller


class View:
    def __init__(self, model: Model, controller: Controller) -> None:
        self._model = model
        self._controller = controller

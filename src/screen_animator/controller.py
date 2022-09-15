import pygame as pg
from .model import Model
from .view import View
from .settings import SettingsManager


class Controller:
    """
    Allows manipulation of the `screen_animator` model.

    Methods
    -------
    init
        Manually perform some initialization.
    run
        Run `screen_animator`.
    """

    def __init__(
        self,
        settings_manager: SettingsManager,
        model: Model,
        display_size: tuple[int, int] = None,
        flipped=False,
    ) -> None:
        """
        Set-up some initial parameters.

        Parameters
        ----------
        settings_manager
            Manages settings.
        model
            The model to manipulate.
        display_size: optional
            Set a custom display size (default is None, full-screen).
        flipped : optional
            Flips the display across the horizontal axis (default is False, not flipped).
        """
        self._settings_manager = settings_manager
        self._settings = self._settings_manager.settings
        self._model = model
        self._view = View(model, self, settings_manager.settings, display_size, flipped)
        self._clock = pg.time.Clock()

    @property
    def initialized(self) -> bool:
        """Are view and model ready to use."""
        return self._view.initialized and self._model.initialized

    def init(self) -> None:
        """Manually finish initializing the controller."""
        self._view.init()
        self._model.init(self._view.perimeter)
        self._model.add_observer(self._view)

    def run(self) -> None:
        """Run `screen_animator` if view and model are ready."""
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
    """
    Checks if the `pygame` event is a quit event.

    Parameters
    ----------
    event
        `pygame` event to be checked.
    Returns
    -------
        True if a quit event, False otherwise.
    """
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
        return True

    return False

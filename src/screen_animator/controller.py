import logging

import pygame as pg

from .model import Model
from .view import View
from .settings import SettingsManager

log = logging.getLogger(__name__)


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
        flipped: bool = False,
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
        self._display_size = display_size
        self._flipped = flipped
        log.info("Creating %s", self)
        self._view = View(
            model, self, settings_manager.settings, self._display_size, self._flipped
        )
        self._clock = pg.time.Clock()

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self._settings_manager},"
            f" {self._model},"
            f" {self._display_size},"
            f" {self._flipped})"
        )

    @property
    def initialized(self) -> bool:
        """Are view and model ready to use."""
        return self._view.initialized and self._model.initialized

    def init(self) -> None:
        """Manually finish initializing the controller."""
        log.info("Finishing initialization of %s", type(self).__name__)
        self._view.init()
        self._model.init(self._view.perimeter)
        self._model.add_observer(self._view)
        log.info("%s initialization complete", type(self).__name__)

    def run(self) -> None:
        """Run `screen_animator` if view and model are ready."""
        log.info(
            "!!! %s%s !!!",
            type(self).__name__,
            " now running, entering main loop".upper(),
        )
        timings_dict = self._settings["timings"]
        while self.initialized:
            self._clock.tick(timings_dict["fps"])
            self._model.update()
            self._check_events()
            timings_dict["fps_actual"] = self._clock.get_fps()

        log.info("Run method complete, %s stopping", type(self).__name__)

    def _check_events(self) -> None:
        for event in pg.event.get():
            if is_quit(event):
                log.info("Telling %s components to quit", type(self).__name__)
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
        log.info("Quit command received")
        return True

    return False

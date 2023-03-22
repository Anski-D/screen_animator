import logging

import pygame as pg

from .observers import Observer
from .model import Model

log = logging.getLogger(__name__)


class View(Observer):
    """
    Display for the `screen_animator` model.

    Attributes
    ----------
    perimeter
        Defines outer perimeter of the display.

    Methods
    -------
    init
        Manually perform some initialization.
    update
        Update the display.
    notify
        Tell the display to update.
    quit
        Set the view as ready to quit.
    """

    perimeter: pg.Rect
    _screen: pg.Surface

    def __init__(
        self,
        model: Model,
        controller: "Controller",
        settings: dict,
        display_size: tuple[int, int] = None,
        flipped: bool = False,
    ) -> None:
        """
        Set-up some initial parameters for the display.

        Parameters
        ----------
        model
            Model to be displayed.
        controller
            Used to manipulate model.
        settings
            User-defined settings.
        display_size : optional
            Set a custom display size (default is None, full-screen).
        flipped : optional
            Flips the display across the horizontal axis (default is False, not flipped).
        """
        self._model = model
        self._controller = controller
        self._settings = settings
        self._display_size = display_size
        self._flipped = flipped
        self._initialized = False

    @property
    def initialized(self) -> bool:
        """Is view ready to use."""
        return self._initialized

    def init(self) -> None:
        """Manually finish initializing the display."""
        log.info("Finishing initialization of %s", type(self).__name__)
        if self._display_size is None:
            self._screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        else:
            self._screen = pg.display.set_mode(self._display_size)
        pg.display.set_caption("Screen_Animator")
        self.perimeter = self._screen.get_rect()
        self._set_bg()
        self._initialized = True
        log.info("%s initialization complete", type(self).__name__)

    def update(self) -> None:
        """Update the display."""
        self._set_bg()
        for group in self._model.item_groups:
            for item in group.sprites():
                self._screen.blit(item.content, item.rect)

        if self._flipped:
            self._screen.blit(pg.transform.rotate(self._screen, 180), (0, 0))

        pg.display.flip()

    def notify(self) -> None:
        """Notify view of change to the model."""
        self.update()

    def quit(self) -> None:
        """Tell view to quit."""
        log.info("%s told to quit", type(self).__name__)
        self._initialized = False

    def _set_bg(self) -> None:
        self._screen.fill(self._settings["bg"]["color"])

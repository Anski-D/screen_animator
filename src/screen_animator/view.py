import logging
from typing import TYPE_CHECKING, Optional

import pygame as pg

from .observers import Observer
from .model import Model

if TYPE_CHECKING:
    from .controller import Controller

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
        flipped : optional
            Flips the display across the horizontal axis (default is False, not flipped).
        """
        self._model = model
        self._controller = controller
        self._settings = settings
        self._flipped = flipped
        self._initialized = False
        log.info("Creating %s", self)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self._model},"
            f" {self._controller},"
            f" {self._settings},"
            f" {self._flipped})"
        )

    @property
    def initialized(self) -> bool:
        """bool: View is ready to use."""
        return self._initialized

    def init(self, display_size: Optional[tuple[int, int]] = None) -> None:
        """
        Manually finish initializing the display.

        Parameters
        ----------
        display_size : optional
            Width and height of window to display on screen, default is fullscreen.
        """
        log.info("Finishing initialization of %s", type(self).__name__)
        if display_size is None:
            self._screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        else:
            self._screen = pg.display.set_mode(display_size)
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

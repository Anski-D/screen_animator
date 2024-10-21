import logging

import pygame as pg

from screen_animator.settings import SettingsManager
from screen_animator.item_groups import ItemGroup

log = logging.getLogger(__name__)


class Model:
    """
    Main engine for `screen_animator`.

    Attributes
    ----------
    item_groups:
        List of aspects to create and update.

    Methods
    -------
    init
        Manually perform some initialization.
    update
        Update the model.
    quit
        Set the model ready to quit.
    """

    item_groups: list[ItemGroup]
    _perimeter: pg.Rect

    def __init__(
        self,
        settings_manager: SettingsManager,
        item_group_types: list[type[ItemGroup]],
    ) -> None:
        """
        Set-up some initial parameters for the model.

        Parameters
        ----------
        settings_manager
            Manage the settings.
        item_group_types
            Class handles for elements of the model.
        """
        super().__init__()

        self._settings_manager = settings_manager
        self._item_group_types = item_group_types
        self._initialized = False
        log.info("Creating %s", self)

        self.update_event_type = 0

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self._settings_manager}, {self._item_group_types})"
        )

    @property
    def initialized(self) -> bool:
        """bool: Model is ready to use."""
        return self._initialized

    def init(self, perimeter: pg.Rect) -> None:
        """
        Manually finish initializing the display.

        Parameters
        ----------
        perimeter
            The outer limits in which the model can operate.
        """
        log.info("Finishing initialization of %s", type(self).__name__)
        self._perimeter = perimeter
        self.item_groups = [
            group(self._settings_manager, self._perimeter)
            for group in self._item_group_types
        ]
        for item_group in self.item_groups:
            item_group.create()

        self._initialized = True
        log.info("%s initialization complete", type(self).__name__)

    def update(self) -> None:
        """Update all aspects of the model."""
        for item_group in self.item_groups:
            item_group.update()

        pg.event.post(pg.Event(self.update_event_type))

    def quit(self) -> None:
        """Set the model as ready to quit."""
        log.info("%s told to quit", type(self).__name__)
        self._initialized = False

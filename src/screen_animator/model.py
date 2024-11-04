import logging
from collections.abc import Iterable, Callable

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
    update_event_type:
        `int` value for update event type.

    Methods
    -------
    update
        Update the model.
    """

    def __init__(
        self,
        settings_manager: SettingsManager,
        item_group_types: Iterable[Callable[[SettingsManager, pg.Rect], ItemGroup]],
        perimeter: pg.Rect,
    ) -> None:
        """
        Set-up some initial parameters for the model.

        Parameters
        ----------
        settings_manager
            Manage the settings.
        item_group_types
            Class handles for elements of the model.
        perimeter
            Outer boundary the model can operate within.
        """
        self._settings_manager = settings_manager
        self._item_group_types = item_group_types
        self._perimeter = perimeter
        log.info("Creating %s", self)

        self.item_groups = [
            group(self._settings_manager, self._perimeter)
            for group in self._item_group_types
        ]
        for item_group in self.item_groups:
            item_group.create()

        self.update_event_type = pg.event.custom_type()
        log.info("%s initialization complete", type(self).__name__)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._settings_manager}, {self._item_group_types}, {self._perimeter})"

    def update(self) -> None:
        """Update all aspects of the model."""
        for item_group in self.item_groups:
            item_group.update()

        pg.event.post(pg.Event(self.update_event_type))

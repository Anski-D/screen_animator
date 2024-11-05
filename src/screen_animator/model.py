import logging
from collections.abc import Iterable, Callable
from enum import Enum, auto

import pygame as pg

from screen_animator.settings import SettingsManager
from screen_animator.item_groups import ItemGroup
from screen_animator.items import Speeder

log = logging.getLogger(__name__)


class Speed(Enum):
    NOTSET = auto()
    RESET = auto()
    FASTER = auto()
    SLOWER = auto()


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


class SpeedChanger:
    _speed_change = 0.1

    def __init__(self, speeder: Speeder) -> None:
        self._speeder = speeder
        log.info("Creating %s", self)

        self._change_speed = {
            Speed.NOTSET: lambda: None,
            Speed.RESET: self.reset,
            Speed.FASTER: self.increase,
            Speed.SLOWER: self.decrease,
        }
        self._speed = self._speeder.speed

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._speeder})"

    def reset(self) -> None:
        self._speeder.speed = self._speed

    def change_speed(self, speed_change: Speed) -> None:
        self._change_speed.get(speed_change, self._change_speed[Speed.NOTSET])()

    def increase(self) -> None:
        self._speeder.speed += int(self._speed_change * self._speed)

    def decrease(self) -> None:
        self._speeder.speed -= int(self._speed_change * self._speed)
        self._speeder.speed = max(0, self._speeder.speed)

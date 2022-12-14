import pygame as pg
from .observers import Observable
from .settings import SettingsManager
from .item_groups import ItemGroup


class Model(Observable):
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

    @property
    def initialized(self) -> bool:
        """Is model ready to use."""
        return self._initialized

    def init(self, perimeter: pg.Rect) -> None:
        """
        Manually finish initializing the display.

        Parameters
        ----------
        perimeter
            The outer limits in which the model can operate.
        """
        self._perimeter = perimeter
        self.item_groups = [
            group(self._settings_manager, self._perimeter)
            for group in self._item_group_types
        ]
        for item_group in self.item_groups:
            item_group.create()

        self._initialized = True

    def update(self) -> None:
        """Update all aspects of the model."""
        for item_group in self.item_groups:
            item_group.update()

        self.notify_observers()

    def quit(self) -> None:
        """Set the model as ready to quit."""
        self._initialized = False

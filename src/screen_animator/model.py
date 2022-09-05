import pygame as pg
from .settings import SettingsManager
from .item_groups import ItemGroup


class Model:
    _perimeter: pg.Rect
    item_groups: list[ItemGroup]

    def __init__(
        self,
        settings_manager: SettingsManager,
        item_group_types: list[type[ItemGroup]],
    ) -> None:
        self._settings_manager = settings_manager
        self._item_group_types = item_group_types
        self._initialized = False

    @property
    def initialized(self) -> bool:
        return self._initialized

    def init(self, perimeter: pg.Rect) -> None:
        self._perimeter = perimeter
        self.item_groups = [
            group(self._settings_manager, self._perimeter)
            for group in self._item_group_types
        ]
        for item_group in self.item_groups:
            item_group.create()

        self._initialized = True

    def update(self) -> None:
        for item_group in self.item_groups:
            item_group.update()

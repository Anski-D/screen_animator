import pygame as pg
from .settings import SettingsManager
from .item_groups import ItemGroup


class Model:
    def __init__(
        self,
        settings_manager: SettingsManager,
        perimeter: pg.Rect,
        item_group_types: list[type[ItemGroup]],
    ) -> None:
        self._settings_manager = settings_manager
        self._perimeter = perimeter
        self._item_groups = [
            group(self._settings_manager.settings, self._perimeter)
            for group in item_group_types
        ]
        self._initialized = False

    @property
    def initialized(self) -> bool:
        return self._initialized

    def init(self) -> None:
        for item_group in self._item_groups:
            item_group.create()

        self._initialized = True

    def update(self) -> None:
        for item_group in self._item_groups:
            item_group.update()

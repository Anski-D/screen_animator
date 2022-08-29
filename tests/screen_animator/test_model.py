import pytest
import pygame as pg
from screen_animator.model import Model
from screen_animator.item_groups import ItemGroup
from screen_animator.settings import SettingsManager


class TestModel:
    @pytest.fixture
    def patch_item_group(self, monkeypatch) -> None:
        """Patch ItemGroup so that its init dunder just returns None."""
        monkeypatch.setattr(ItemGroup, "__init__", lambda x, y, z: None)
        ItemGroup.__abstractmethods__ = set()

    def test_init_item_group(
        self,
        example_settings_manager: SettingsManager,
        example_perimeter: pg.Rect,
        patch_item_group,
    ) -> None:
        """init dunder creates ItemGroup instances."""
        model = Model(example_settings_manager, example_perimeter, [ItemGroup])

        assert all(
            isinstance(item_group, ItemGroup) for item_group in model.item_groups
        )

    def test_init_initialized_set(
        self,
        monkeypatch,
        example_settings_manager: SettingsManager,
        example_perimeter: pg.Rect,
    ) -> None:
        """Set initialized attribute to True."""
        monkeypatch.setattr(ItemGroup, "__init__", lambda x, y, z: None)
        monkeypatch.setattr(ItemGroup, "create", lambda x: None)
        model = Model(example_settings_manager, example_perimeter, [ItemGroup])
        model.init()

        assert model.initialized

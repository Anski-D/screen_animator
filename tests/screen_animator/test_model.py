import pytest
import pygame as pg

from screen_animator.model import Model
from screen_animator.item_groups import ItemGroup
from screen_animator.settings import SettingsManager


class TestModel:
    @pytest.fixture
    def patch_item_group_type(self, monkeypatch) -> None:
        """Patch ItemGroup so that its init dunder just returns None."""
        monkeypatch.setattr(ItemGroup, "__init__", lambda *args, **kwargs: None)
        ItemGroup.__abstractmethods__ = set()

    @pytest.fixture
    def example_model(
        self,
        example_settings_manager: SettingsManager,
        example_perimeter: pg.Rect,
        patch_item_group_type,
    ) -> Model:
        """Create example Model"""
        return Model(
            example_settings_manager, [ItemGroup for _ in range(3)], example_perimeter
        )

    def test_init_item_group(self, example_model: Model) -> None:
        """init dunder creates ItemGroup instances."""
        model = example_model

        assert all(
            isinstance(item_group, ItemGroup) for item_group in model.item_groups
        )

    def test_init_event_type_int(self, example_model: Model) -> None:
        """Update event type is `int`."""
        model = example_model

        assert isinstance(model.update_event_type, int)

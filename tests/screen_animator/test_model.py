import pytest
from screen_animator.model import Model
from screen_animator.item_groups import ItemGroup


class TestModel:
    def test_init_item_group(self, monkeypatch, example_settings_manager, example_perimeter):
        monkeypatch.setattr(ItemGroup, "__init__", lambda x, y, z: None)
        ItemGroup.__abstractmethods__ = set()
        model = Model(example_settings_manager, example_perimeter, [ItemGroup])

        assert all(isinstance(item_group, ItemGroup) for item_group in model.item_groups)
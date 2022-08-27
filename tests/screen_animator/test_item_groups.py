import pytest
import pygame as pg
from screen_animator.settings import SettingsManager
from screen_animator.item_groups import LeftScrollingText


class TestLeftScrollingText:
    @pytest.fixture
    def example_left_scrolling_text(self, monkeypatch, example_settings_dict_with_tuples, example_perimeter):
        pg.init()
        monkeypatch.setattr(
            SettingsManager,
            "_import_settings",
            lambda x, y: example_settings_dict_with_tuples,
        )
        settings_manager = SettingsManager(None, None)

        return LeftScrollingText(settings_manager.settings, example_perimeter)

    @pytest.mark.parametrize("num_of_items", [1, 2, 3, 5, 8])
    def test_create(self, num_of_items, example_left_scrolling_text):
        item_group = example_left_scrolling_text

        for _ in range(num_of_items):
            item_group.create()

        assert len(item_group._group) == num_of_items

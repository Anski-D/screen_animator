import pytest
import pygame as pg
import math
from screen_animator.settings import SettingsManager
from screen_animator.item_groups import LeftScrollingTextGroup


class TestLeftScrollingTextGroup:
    @pytest.fixture
    def example_left_scrolling_text(
        self, monkeypatch, example_settings_dict_with_tuples, example_perimeter
    ):
        pg.init()
        monkeypatch.setattr(
            SettingsManager,
            "_import_settings",
            lambda x, y: example_settings_dict_with_tuples,
        )
        settings_manager = SettingsManager(None, None)

        return LeftScrollingTextGroup(settings_manager.settings, example_perimeter)

    @pytest.mark.parametrize("num_of_items", [1, 2, 3, 5, 8])
    def test_create(self, num_of_items, example_left_scrolling_text):
        item_group = example_left_scrolling_text

        for _ in range(num_of_items):
            item_group.create()

        assert len(item_group._group) == num_of_items

    def test_create_position(self, example_left_scrolling_text, example_perimeter):
        item_group = example_left_scrolling_text
        item_group.create()

        assert item_group._group.sprites()[0].rect_box.left == example_perimeter.right

    def test_update_create(self, example_left_scrolling_text):
        item_group = example_left_scrolling_text
        item_group.create()
        item = item_group._group.sprites()[0]
        width = item.rect_box.width
        speed = 100
        item._movement._speed = speed
        for _ in range(math.ceil(width / speed)):
            item_group.update()

        assert len(item_group._group.sprites()) == 2

    def test_update_delete(self, monkeypatch, example_left_scrolling_text):
        item_group = example_left_scrolling_text
        item_group.create()
        item = item_group._group.sprites()[0]
        width = item.rect_box.width + item_group._perimeter.width
        speed = 100
        item._movement._speed = speed
        monkeypatch.setattr(LeftScrollingTextGroup, "create", lambda x: None)
        for _ in range(math.ceil(width / speed)):
            item_group.update()

        assert len(item_group._group.sprites()) == 0

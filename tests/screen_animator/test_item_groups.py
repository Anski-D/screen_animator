import math
import time
import pytest
import pygame as pg
from screen_animator.settings import SettingsManager
from screen_animator.item_groups import (
    LeftScrollingTextGroup,
    RandomImagesGroup,
    ColorChangeGroup,
)


@pytest.fixture
def example_settings_manager(
    monkeypatch, example_settings_dict_with_tuples: dict, example_content: pg.Surface
) -> SettingsManager:
    pg.init()
    settings_dict = example_settings_dict_with_tuples
    monkeypatch.setattr(
        SettingsManager,
        "_import_settings",
        lambda x, y: settings_dict,
    )
    monkeypatch.setattr(SettingsManager, "_load_images", lambda x: None)
    settings_manager = SettingsManager(None, None)
    settings_manager.settings["images"]["images"] = [
        example_content
        for _ in range(len(example_settings_dict_with_tuples["images"]["sources"]))
    ]
    return settings_manager


class TestLeftScrollingTextGroup:
    @pytest.fixture
    def example_left_scrolling_text_group(
        self, example_settings_manager: SettingsManager, example_perimeter: pg.Rect
    ) -> LeftScrollingTextGroup:
        return LeftScrollingTextGroup(example_settings_manager, example_perimeter)

    @pytest.mark.parametrize("num_of_items", [1, 2, 3, 5, 8])
    def test_create_no_outline(
        self,
        num_of_items: int,
        example_left_scrolling_text_group: LeftScrollingTextGroup,
    ) -> None:
        item_group = example_left_scrolling_text_group
        item_group._settings["messages"]["outline_width"] = 0

        for _ in range(num_of_items):
            item_group.create()

        assert len(item_group.items) == num_of_items

    @pytest.mark.parametrize("num_of_items", [1, 2, 3, 5, 8])
    def test_create_with_outline(
        self,
        num_of_items: int,
        example_left_scrolling_text_group: LeftScrollingTextGroup,
    ) -> None:
        item_group = example_left_scrolling_text_group

        for _ in range(num_of_items):
            item_group.create()

        assert len(item_group.items) == num_of_items + 8 * num_of_items

    def test_create_position(
        self,
        example_left_scrolling_text_group: LeftScrollingTextGroup,
        example_perimeter: pg.Rect,
    ) -> None:
        item_group = example_left_scrolling_text_group
        item_group.create()

        assert item_group.items[7].rect.left == example_perimeter.right

    def test_update_create(
        self, monkeypatch, example_left_scrolling_text_group: LeftScrollingTextGroup
    ) -> None:
        monkeypatch.setattr(LeftScrollingTextGroup, "_set_speed", lambda x: None)
        item_group = example_left_scrolling_text_group
        item_group._settings["messages"]["outline_width"] = 0
        item_group.create()
        item = item_group.items[0]
        width = item.rect.width
        speed = 100
        item._movement._speed = speed
        for _ in range(math.ceil(width / speed)):
            item_group.update()

        assert len(item_group.items) == 2

    def test_update_delete(
        self, monkeypatch, example_left_scrolling_text_group: LeftScrollingTextGroup
    ) -> None:
        monkeypatch.setattr(LeftScrollingTextGroup, "_set_speed", lambda x: None)
        item_group = example_left_scrolling_text_group
        item_group.create()
        item = item_group.items[0]
        width = item.rect.width + item_group._perimeter.width
        speed = 100
        item._movement._speed = speed
        monkeypatch.setattr(LeftScrollingTextGroup, "create", lambda x: None)
        for _ in range(math.ceil(width / speed)):
            item_group.update()

        assert len(item_group.items) == 0

    def test_generate_message(
        self, example_left_scrolling_text_group: LeftScrollingTextGroup
    ) -> None:
        assert isinstance(
            example_left_scrolling_text_group._generate_message("Test"), pg.Surface
        )

    def test_set_outline(
        self, example_left_scrolling_text_group: LeftScrollingTextGroup
    ) -> None:
        item_group = example_left_scrolling_text_group
        item_group._set_outline("Test")

        assert len(item_group.items) == 8


class TestRandomImagesGroup:
    @pytest.fixture
    def example_random_images_group(
        self, example_settings_manager: SettingsManager, example_perimeter: pg.Rect
    ) -> RandomImagesGroup:
        return RandomImagesGroup(example_settings_manager, example_perimeter)

    def test_create(
        self,
        example_random_images_group: RandomImagesGroup,
        example_settings_dict_with_tuples: dict,
    ) -> None:
        item_group = example_random_images_group
        item_group.create()
        image_settings = example_settings_dict_with_tuples["images"]

        assert (
            len(item_group.items)
            == len(image_settings["sources"]) * image_settings["number"]
        )

    @pytest.mark.parametrize("repeats", [1, 2, 3, 5, 8])
    def test_update(
        self, repeats: int, example_random_images_group: RandomImagesGroup
    ) -> None:
        item_group = example_random_images_group
        item_group.create()
        for _ in range(repeats):
            item_group.update()

        assert all(
            [item_group._perimeter.contains(image) for image in item_group.items]
        )


class TestColorChangeGroup:
    @pytest.fixture
    def example_color_change_group(
        self, example_settings_manager: SettingsManager, example_perimeter: pg.Rect
    ) -> ColorChangeGroup:
        return ColorChangeGroup(example_settings_manager, example_perimeter)

    def test_create(self, example_color_change_group: ColorChangeGroup) -> None:
        item_group = example_color_change_group
        item_group.create()

        assert isinstance(item_group._time, int)

    @pytest.mark.slow
    @pytest.mark.parametrize(
        "sleep, output", [(1, True), (2, True), (3, True), (5, False), (8, False)]
    )
    def test_update(
        self, sleep: int, output: bool, example_color_change_group: ColorChangeGroup
    ) -> None:
        item_group = example_color_change_group
        item_group._settings["timings"]["color_change_time"] = 4
        item_group.create()
        time1 = item_group._time
        time.sleep(sleep)
        item_group.update()
        time2 = item_group._time

        assert (time1 == time2) is output

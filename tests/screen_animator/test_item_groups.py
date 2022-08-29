import math
import pytest
import pygame as pg
from screen_animator.settings import SettingsManager
from screen_animator.item_groups import LeftScrollingTextGroup, RandomImagesGroup


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
        return LeftScrollingTextGroup(
            example_settings_manager.settings, example_perimeter
        )

    @pytest.mark.parametrize("num_of_items", [1, 2, 3, 5, 8])
    def test_create(
        self,
        num_of_items: int,
        example_left_scrolling_text_group: LeftScrollingTextGroup,
    ) -> None:
        item_group = example_left_scrolling_text_group

        for _ in range(num_of_items):
            item_group.create()

        assert len(item_group._group) == num_of_items

    def test_create_position(
        self,
        example_left_scrolling_text_group: LeftScrollingTextGroup,
        example_perimeter: pg.Rect,
    ) -> None:
        item_group = example_left_scrolling_text_group
        item_group.create()

        assert item_group._group.sprites()[0].rect.left == example_perimeter.right

    def test_update_create(
        self, example_left_scrolling_text_group: LeftScrollingTextGroup
    ) -> None:
        item_group = example_left_scrolling_text_group
        item_group.create()
        item = item_group._group.sprites()[0]
        width = item.rect.width
        speed = 100
        item._movement._speed = speed
        for _ in range(math.ceil(width / speed)):
            item_group.update()

        assert len(item_group._group.sprites()) == 2

    def test_update_delete(
        self, monkeypatch, example_left_scrolling_text_group: LeftScrollingTextGroup
    ) -> None:
        item_group = example_left_scrolling_text_group
        item_group.create()
        item = item_group._group.sprites()[0]
        width = item.rect.width + item_group._perimeter.width
        speed = 100
        item._movement._speed = speed
        monkeypatch.setattr(LeftScrollingTextGroup, "create", lambda x: None)
        for _ in range(math.ceil(width / speed)):
            item_group.update()

        assert len(item_group._group.sprites()) == 0


class TestRandomImagesGroup:
    @pytest.fixture
    def example_random_images_group(
        self, example_settings_manager: SettingsManager, example_perimeter: pg.Rect
    ) -> RandomImagesGroup:
        return RandomImagesGroup(example_settings_manager.settings, example_perimeter)

    def test_create(
        self,
        example_random_images_group: RandomImagesGroup,
        example_settings_dict_with_tuples: dict,
    ) -> None:
        item_group = example_random_images_group
        item_group.create()
        image_settings = example_settings_dict_with_tuples["images"]

        assert (
            len(item_group._group.sprites())
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
            [
                item_group._perimeter.contains(image)
                for image in item_group._group.sprites()
            ]
        )

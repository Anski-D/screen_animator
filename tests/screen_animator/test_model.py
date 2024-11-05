from collections.abc import Callable

import pytest
import pygame as pg

from screen_animator.model import Model, SpeedChanger, Speed
from screen_animator.item_groups import ItemGroup
from screen_animator.settings import SettingsManager
from screen_animator.items import Speeder, ScrollingMovement


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


class TestSpeedChanger:
    @pytest.fixture
    def example_scrolling_movement(self) -> ScrollingMovement:
        """Create example `Speeder`."""
        speeder = ScrollingMovement()
        speeder.speed = 400

        return speeder

    @pytest.fixture
    def example_speed_changer(
        self, example_scrolling_movement: Speeder
    ) -> SpeedChanger:
        """Create example `SpeedChanger`."""
        return SpeedChanger(example_scrolling_movement)

    @pytest.mark.parametrize("repeat", [1, 2, 3, 5, 8, 13])
    def test_increase_speed(self, repeat, example_speed_changer: SpeedChanger) -> None:
        """Speed of `Speeder` is increased."""
        speed_changer = example_speed_changer
        speed_initial = speed_changer._speeder.speed
        for _ in range(repeat):
            speed_changer.increase()

        assert speed_changer._speeder.speed == speed_initial + int(
            repeat * speed_changer._speed_change * speed_initial
        )

    @pytest.mark.parametrize(
        "repeats, result", [(1, 1), (2, 2), (3, 3), (5, 5), (8, 8), (10, 0), (13, 0)]
    )
    def test_decrease_speed(
        self, repeats: int, result: int, example_speed_changer: SpeedChanger
    ) -> None:
        """Speed of `Speeder` is decreased."""
        speed_changer = example_speed_changer
        speed_initial = speed_changer._speeder.speed
        for _ in range(repeats):
            speed_changer.decrease()

        assert speed_changer._speeder.speed == (
            (result and 1 * speed_initial)
            - int(result * speed_changer._speed_change * speed_initial)
        )

    def test_reset_speed(self, example_speed_changer: SpeedChanger) -> None:
        """Speed of `Speeder` is reset."""
        speed_changer = example_speed_changer
        speed_initial = speed_changer._speeder.speed
        for _ in range(10):
            speed_changer.increase()

        speed_interim = speed_changer._speeder.speed
        speed_changer.reset()

        assert all(
            [
                speed_interim != speed_initial,
                speed_changer._speeder.speed == speed_initial,
            ]
        )

    @pytest.mark.parametrize(
        "speed_input, check_method",
        [(Speed.FASTER, int.__gt__), (Speed.SLOWER, int.__lt__)],
    )
    def test_change_speed_changes(
        self,
        speed_input: Speed,
        check_method: Callable[[int, int], bool],
        example_speed_changer: SpeedChanger,
    ) -> None:
        """Speed of `Speeder` is changed."""
        speed_changer = example_speed_changer
        speed_initial = speed_changer._speeder.speed
        speed_changer.change_speed(speed_input)

        assert check_method(speed_changer._speeder.speed, speed_initial)

    def test_change_speed_reset(self, example_speed_changer: SpeedChanger) -> None:
        """Speed of `Speeder` is reset."""
        speed_changer = example_speed_changer
        speed_initial = speed_changer._speeder.speed
        for _ in range(10):
            speed_changer.increase()

        speed_interim = speed_changer._speeder.speed
        speed_changer.change_speed(Speed.RESET)

        assert all(
            [
                speed_interim != speed_initial,
                speed_changer._speeder.speed == speed_initial,
            ]
        )

    @pytest.mark.parametrize("speed_input", [Speed.NOTSET, ""])
    def test_change_speed_do_nothing(
        self, speed_input: Speed | str, example_speed_changer: SpeedChanger
    ) -> None:
        """Speed of `Speeder` is left as-is."""
        speed_changer = example_speed_changer
        speed_initial = speed_changer._speeder.speed
        for _ in range(10):
            speed_changer.increase()

        speed_interim = speed_changer._speeder.speed
        speed_changer.change_speed(speed_input)

        assert all(
            [
                speed_changer._speeder.speed != speed_initial,
                speed_changer._speeder.speed == speed_interim,
            ]
        )

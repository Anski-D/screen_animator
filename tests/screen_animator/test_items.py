import pygame as pg
import pytest
from screen_animator.items import Item, ScrollingMovement, RandomMovement


@pytest.fixture
def example_item(example_content, example_perimeter):
    Item.__abstractmethods__ = set()

    return Item(pg.sprite.Group(), example_content, example_perimeter)


class TestItem:
    def test_content_return_type(self, example_item):
        assert isinstance(example_item.content, pg.Surface)

    def test_content_setter(self, example_item):
        assert example_item.rect == pg.Rect(0, 0, 20, 10)


class TestScrollingMovement:
    @pytest.mark.parametrize(
        "direction, output",
        [
            ("up", ("y", -1)),
            ("right", ("x", 1)),
            ("down", ("y", 1)),
            ("left", ("x", -1)),
            ("test", ("x", -1)),
        ],
    )
    def test_direction_setter(self, direction, output):
        movement = ScrollingMovement()
        movement.direction = direction

        assert movement._axis, movement._sign == output

    @pytest.mark.parametrize(
        "speed, direction, axis, value",
        [
            (1, "up", "y", 248),
            (2, "right", "x", 504),
            (3, "down", "y", 256),
            (5, "left", "x", 490),
        ],
    )
    def test_move(self, speed, direction, axis, value, example_item):
        item = example_item
        item.rect.topleft = item.perimeter.center
        movement = ScrollingMovement(speed, direction)
        movement.move(item)
        movement.move(item)

        assert getattr(item.rect, axis) == value


class TestRandomMovement:
    @pytest.mark.parametrize("repeat", range(5))
    def test_move_perimeter_contains(self, repeat, example_item):
        item = example_item
        movement = RandomMovement()
        movement.move(item)

        assert item.perimeter.contains(item.rect)

    def test_move_repeat_move(self, example_item):
        item = example_item
        movement = RandomMovement()
        movement.move(item)
        rect1 = item.rect.copy()
        movement.move(item)

        assert item.rect != rect1

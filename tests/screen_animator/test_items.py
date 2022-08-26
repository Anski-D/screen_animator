import pygame as pg
import pytest
from screen_animator.items import Movable, Item, ScrollingMovement, RandomMovement


@pytest.fixture
def example_perimeter():
    return pg.Rect(0, 0, 1000, 500)


@pytest.fixture
def example_content():
    return pg.Surface((20, 10))


@pytest.fixture
def example_item(example_content, example_perimeter):
    return Item(pg.sprite.Group(), example_content, example_perimeter)


@pytest.fixture
def example_movable(example_perimeter):
    Movable.__abstractmethods__ = set()
    movable = Movable()
    movable.rect_box = pg.Rect(100, 50, 20, 10)
    movable.perimeter = example_perimeter

    return movable


class TestItem:
    def test_content_return_type(self, example_item):
        assert isinstance(example_item.content, pg.Surface)

    def test_content_setter(self, example_item):
        assert example_item._rect == pg.Rect(0, 0, 20, 10)


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
            (1, "up", "y", 48),
            (2, "right", "x", 104),
            (3, "down", "y", 56),
            (5, "left", "x", 90),
        ],
    )
    def test_move(self, example_movable, speed, direction, axis, value):
        movable = example_movable
        movement = ScrollingMovement(speed, direction)
        movement.move(movable)
        movement.move(movable)
        rect = movable.rect_box

        assert getattr(rect, axis) == value


class TestRandomMovement:
    @pytest.mark.parametrize("repeat", range(5))
    def test_move_perimeter_contains(self, repeat, example_movable):
        movable = example_movable
        movement = RandomMovement()
        movement.move(movable)

        assert movable.perimeter.contains(movable.rect_box)

    def test_move_repeat_move(self, example_movable):
        movable = example_movable
        movement = RandomMovement()
        movement.move(movable)
        rect1 = movable.rect_box.copy()
        movement.move(movable)

        assert movable.rect_box != rect1

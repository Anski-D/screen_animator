import pygame as pg
import pytest
from screen_animator.items import Item, ScrollingMovement


@pytest.fixture
def example_perimeter():
    return pg.Rect(0, 0, 1000, 500)


@pytest.fixture
def example_content():
    return pg.Surface((20, 10))


@pytest.fixture
def setup_item(example_content, example_perimeter):
    return Item(pg.sprite.Group(), example_content, example_perimeter)


class TestItem:
    def test_content_return_type(self, setup_item):
        assert isinstance(setup_item.content, pg.Surface)

    def test_content_setter(self, setup_item):
        assert setup_item._rect == pg.Rect(0, 0, 20, 10)


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
    def test_set_direction(self, direction, output):
        movement = ScrollingMovement()

        assert movement._set_direction(direction) == output

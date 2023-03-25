import pygame as pg
import pytest
from screen_animator.settings import SettingsManager


@pytest.fixture
def example_settings_dict() -> dict:
    """Provide example settings dict prior to conversion to tuples."""
    return {
        "colors": [
            [255, 0, 0],
            [0, 255, 0],
            [0, 0, 255],
        ],
        "messages": {
            "messages": [
                "TEST MESSAGE 1!",
                "TEST MESSAGE 2!",
                "TEST MESSAGE 3!",
                "TEST MESSAGE 4!",
            ],
            "separator": "    ",
            "typeface": "freeserif",
            "size": 350,
            "bold": True,
            "italic": False,
            "anti-aliasing": False,
            "scroll_speed": 240,
            "outline_width": 3,
            "outline_copies": 12,
            "outline_colors": [
                [0, 0, 0],
                [255, 255, 255],
            ],
        },
        "images": {
            "sources": [
                ["pic1.svg", 64],
                ["pic2.bmp", -1],
                ["pic3.bmp", 64],
            ],
            "number": 10,
            "reposition_attempts": -1,
        },
        "timings": {
            "fps": 30,
            "image_change_time": 2,
            "color_change_time": 15,
        },
    }


@pytest.fixture
def example_settings_dict_with_tuples(example_settings_dict: dict) -> dict:
    """Provide example settings dict after conversion to tuples."""
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
    ]
    outline_colors = [
        (0, 0, 0),
        (255, 255, 255),
    ]
    sources = [
        ("pic1.svg", 64),
        ("pic2.bmp", -1),
        ("pic3.bmp", 64),
    ]
    example_settings_dict["colors"] = colors
    example_settings_dict["messages"]["outline_colors"] = outline_colors
    example_settings_dict["images"]["sources"] = sources

    return example_settings_dict


@pytest.fixture
def example_perimeter() -> pg.Rect:
    """Provide example perimeter."""
    return pg.Rect(0, 0, 1000, 500)


@pytest.fixture
def example_content() -> pg.Surface:
    """Provide example content surface."""
    return pg.Surface((20, 10))


@pytest.fixture
def example_settings_manager(
    monkeypatch, example_settings_dict_with_tuples: dict
) -> SettingsManager:
    """Provide an initialised `SettingsManager`."""
    pg.init()
    monkeypatch.setattr(
        SettingsManager,
        "_import_settings",
        lambda x, y: example_settings_dict_with_tuples,
    )
    monkeypatch.setattr(SettingsManager, "_setup_settings", lambda x: None)

    return SettingsManager(None, None)

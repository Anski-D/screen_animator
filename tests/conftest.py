import pytest


@pytest.fixture
def example_settings_dict():
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
            "scroll_speed": 240.0,
            "outline_width": 3,
            "outline_colors": [
                [0, 0, 0],
                [255, 255, 255],
            ],
        },
        "images": {
            "sources": [
                "pic1.bmp",
                "pic2.bmp",
                "pic3.bmp",
            ],
            "number": 10,
        },
        "timings": {
            "fps": 30,
            "image_change_time": 2,
            "color_change_time": 15,
        },
    }


@pytest.fixture
def example_settings_dict_with_tuples(example_settings_dict):
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
    ]
    outline_colors = [
        (0, 0, 0),
        (255, 255, 255),
    ]
    example_settings_dict["colors"] = colors
    example_settings_dict["messages"]["outline_colors"] = outline_colors

    return example_settings_dict

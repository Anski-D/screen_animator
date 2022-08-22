import pytest
import pygame as pg
from screen_animator.settings import SettingsImporter, SettingsManager


@pytest.fixture
def example_settings_dict():
    return {
        "colours": [
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
            "outline_colours": [
                [0, 0, 0],
                [255, 255, 255],
            ], },
        "images": {
            "sources": [
                "pic1.bmp",
                "pic2.bmp",
                "pic3.bmp",
            ],
            "number": 10, },
        "timings": {
            "fps": 30,
            "image_change_time": 2,
            "colour_change_time": 15, }
    }


class TestSettingsImporter:
    def test_validate_settings_raises_value_error(self, example_settings_dict):
        del example_settings_dict["colours"]
        importer = SettingsImporter()
        importer._settings = example_settings_dict
        with pytest.raises(ValueError):
            importer._validate_settings()

    def test_validate_settings_passes(self, example_settings_dict):
        importer = SettingsImporter()
        importer._settings = example_settings_dict
        assert importer._validate_settings() is None


class TestSettingsManager:
    @pytest.fixture
    def setup_settings_manager(self, monkeypatch, example_settings_dict):
        pg.init()
        monkeypatch.setattr(SettingsManager, '_import_settings', lambda x, y: example_settings_dict)

        return SettingsManager(None, None)

    @pytest.mark.parametrize('group', ['bg', 'messages'])
    def test_set_colours(self, group, setup_settings_manager):
        settings_manager = setup_settings_manager
        settings_manager.set_colours()

        assert settings_manager.settings[group]['colour'] in settings_manager.settings['colours']

    def test_set_outline_colour(self, setup_settings_manager):
        settings_manager = setup_settings_manager
        settings_manager.set_colours()

        assert settings_manager.settings['messages']['outline_colour'] \
               in settings_manager.settings['messages']['outline_colours']

    def test_set_font(self, setup_settings_manager):
        settings_manager = setup_settings_manager
        settings_manager._set_font()

        assert isinstance(settings_manager.settings['messages']['font'], pg.font.Font)

    @pytest.mark.parametrize('repeat', range(5))
    def test_generate_text(self, repeat, setup_settings_manager, example_settings_dict):
        settings_manager = setup_settings_manager

        assert settings_manager._generate_message_text() \
               in [
                   f'{message}{example_settings_dict["messages"]["separator"]}'
                   for message
                   in example_settings_dict["messages"]["messages"]
               ]

    def test_generate_text_return_type(self, setup_settings_manager):
        settings_manager = setup_settings_manager

        assert isinstance(settings_manager._generate_message_text(), str)

    def test_generate_message(self, setup_settings_manager):
        settings_manager = setup_settings_manager
        messages_dict = settings_manager._settings['messages']
        messages_dict['colour'] = [0, 0, 0]
        messages_dict['font'] = pg.font.Font(None, 10)

        assert isinstance(settings_manager._generate_message(), pg.Surface)

    def test_load_images(self, monkeypatch, setup_settings_manager, example_settings_dict):
        monkeypatch.setattr(pg.image, 'load', lambda x: pg.Surface((20, 10)))
        settings_manager = setup_settings_manager
        settings_manager._load_images()
        images_dict = settings_manager.settings['images']

        assert len(images_dict['images']) == len(images_dict['sources'])

    @pytest.mark.xfail
    def test_load_images_raises_file_not_found_error(self, setup_settings_manager):
        settings_manager = setup_settings_manager
        with pytest.raises(FileNotFoundError):
            settings_manager._load_images()

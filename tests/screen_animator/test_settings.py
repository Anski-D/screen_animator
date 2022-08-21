import pytest
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
    def test_validate_settings_value_error(self, example_settings_dict):
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
    def setup_settings_manager(self, example_settings_dict, monkeypatch):
        monkeypatch.setattr(SettingsManager, '_import_settings', lambda x, y: example_settings_dict)
        return SettingsManager(None, None)

    @pytest.mark.parametrize('group', ['bg', 'messages'])
    def test_set_colours(self, setup_settings_manager, group):
        settings_manager = setup_settings_manager
        settings_manager.set_colours()

        assert settings_manager.settings[group]['colour'] in settings_manager.settings['colours']

    def test_set_outline_colour(self, setup_settings_manager):
        settings_manager = setup_settings_manager
        settings_manager.set_colours()

        assert settings_manager.settings['messages']['outline_colour'] \
               in settings_manager.settings['messages']['outline_colours']


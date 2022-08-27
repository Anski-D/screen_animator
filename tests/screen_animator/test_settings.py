import pytest
import pygame as pg
from screen_animator.settings import SettingsImporter, SettingsManager


class TestSettingsImporter:
    def test_validate_settings_raises_value_error(self, example_settings_dict):
        del example_settings_dict["colors"]
        importer = SettingsImporter()
        importer._settings = example_settings_dict
        with pytest.raises(ValueError):
            importer._validate_settings()

    def test_validate_settings_passes(self, example_settings_dict):
        importer = SettingsImporter()
        importer._settings = example_settings_dict
        assert importer._validate_settings() is None

    def test_convert_colors_to_tuples(
        self, example_settings_dict, example_settings_dict_with_tuples
    ):
        importer = SettingsImporter()

        assert (
            importer._convert_colors_to_tuples(example_settings_dict)
            == example_settings_dict_with_tuples
        )


class TestSettingsManager:
    @pytest.fixture
    def setup_settings_manager(self, monkeypatch, example_settings_dict_with_tuples):
        pg.init()
        monkeypatch.setattr(
            SettingsManager,
            "_import_settings",
            lambda x, y: example_settings_dict_with_tuples,
        )
        monkeypatch.setattr(SettingsManager, "_setup_settings", lambda x: None)

        return SettingsManager(None, None)

    @pytest.mark.parametrize("group", ["bg", "messages"])
    def test_set_colors(self, group, setup_settings_manager):
        settings_manager = setup_settings_manager
        settings_manager.set_colors()

        assert (
            settings_manager.settings[group]["color"]
            in settings_manager.settings["colors"]
        )

    def test_set_outline_color(self, setup_settings_manager):
        settings_manager = setup_settings_manager
        settings_manager.set_colors()

        assert (
            settings_manager.settings["messages"]["outline_color"]
            in settings_manager.settings["messages"]["outline_colors"]
        )

    def test_set_font(self, setup_settings_manager):
        settings_manager = setup_settings_manager
        settings_manager._set_font()

        assert isinstance(settings_manager.settings["messages"]["font"], pg.font.Font)

    @pytest.mark.parametrize("repeat", range(5))
    def test_generate_text(
        self, repeat, setup_settings_manager, example_settings_dict_with_tuples
    ):
        settings_manager = setup_settings_manager

        assert settings_manager._generate_message_text() in [
            f'{message}{example_settings_dict_with_tuples["messages"]["separator"]}'
            for message in example_settings_dict_with_tuples["messages"]["messages"]
        ]

    def test_generate_text_return_type(self, setup_settings_manager):
        settings_manager = setup_settings_manager

        assert isinstance(settings_manager._generate_message_text(), str)

    def test_generate_message(self, setup_settings_manager):
        settings_manager = setup_settings_manager
        messages_dict = settings_manager._settings["messages"]
        messages_dict["color"] = [0, 0, 0]
        messages_dict["font"] = pg.font.Font(None, 10)

        assert isinstance(settings_manager._generate_message(), pg.Surface)

    def test_load_images(
        self, monkeypatch, setup_settings_manager, example_settings_dict_with_tuples
    ):
        monkeypatch.setattr(pg.image, "load", lambda x: pg.Surface((20, 10)))
        settings_manager = setup_settings_manager
        settings_manager._load_images()
        images_dict = settings_manager.settings["images"]

        assert len(images_dict["images"]) == len(
            example_settings_dict_with_tuples["images"]["sources"]
        )

    def test_load_images_file_not_found_error_not_raised(self, setup_settings_manager):
        settings_manager = setup_settings_manager
        try:
            settings_manager._load_images()
        except FileNotFoundError as error:
            assert False, f"{error}"

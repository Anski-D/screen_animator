import pytest
import pygame as pg
from screen_animator.settings import SettingsImporter, SettingsManager


class TestSettingsImporter:
    def test_validate_settings_raises_value_error(
        self, example_settings_dict: dict
    ) -> None:
        """Raise `ValueError` if input settings do not match prescribed format."""
        del example_settings_dict["colors"]
        importer = SettingsImporter()
        importer._settings = example_settings_dict
        with pytest.raises(ValueError):
            importer._validate_settings()

    def test_validate_settings_passes(self, example_settings_dict: dict) -> None:
        """Correctly formatted settings input successfully validates."""
        importer = SettingsImporter()
        importer._settings = example_settings_dict

        assert importer._validate_settings() is None

    def test_convert_colors_to_tuples(
        self, example_settings_dict: dict, example_settings_dict_with_tuples: dict
    ) -> None:
        """Lists of a certain format are converted to tuples."""
        importer = SettingsImporter()

        assert (
            importer._convert_colors_to_tuples(example_settings_dict)
            == example_settings_dict_with_tuples
        )


class TestSettingsManager:
    @pytest.mark.parametrize("group", ["bg", "messages"])
    def test_set_colors(
        self, group: pg.sprite.Group, example_settings_manager: SettingsManager
    ) -> None:
        """Colors are set to a color option provided in settings."""
        settings_manager = example_settings_manager
        settings_manager.set_colors()
        settings = settings_manager.settings

        assert settings[group]["color"] in settings["colors"]

    def test_set_outline_color(self, example_settings_manager: SettingsManager) -> None:
        """Outline color set to color option provided in settings."""
        settings_manager = example_settings_manager
        settings_manager.set_colors()
        messages_dict = settings_manager.settings["messages"]

        assert messages_dict["outline_color"] in messages_dict["outline_colors"]

    def test_set_outline_colour_single_choice(
        self, example_settings_manager: SettingsManager
    ) -> None:
        """Outline color set correctly when only a single option provided."""
        settings_manager = example_settings_manager
        outline_color = (0, 255, 0)
        messages_dict = settings_manager.settings["messages"]
        messages_dict["outline_colors"] = outline_color
        settings_manager.set_colors()

        assert messages_dict["outline_color"] == outline_color

    def test_set_font(self, example_settings_manager: SettingsManager) -> None:
        """`Font` instance created and added to settings."""
        settings_manager = example_settings_manager
        settings_manager._set_font()

        assert isinstance(settings_manager.settings["messages"]["font"], pg.font.Font)

    @pytest.mark.parametrize("repeat", range(5))
    def test_generate_text(
        self,
        repeat: int,
        example_settings_manager: SettingsManager,
        example_settings_dict_with_tuples: dict,
    ) -> None:
        """Concatenated message strings are generated."""
        settings_manager = example_settings_manager
        messages_dict = example_settings_dict_with_tuples["messages"]

        assert settings_manager.generate_message_text() in [
            f'{message}{messages_dict["separator"]}'
            for message in messages_dict["messages"]
        ]

    def test_generate_text_return_type(
        self, example_settings_manager: SettingsManager
    ) -> None:
        """Message strings generated are of correct type."""
        settings_manager = example_settings_manager

        assert isinstance(settings_manager.generate_message_text(), str)

    def test_load_images(
        self,
        monkeypatch,
        example_settings_manager: SettingsManager,
        example_settings_dict_with_tuples: dict,
    ) -> None:
        """Images are loaded and stored in settings."""
        monkeypatch.setattr(pg.image, "load", lambda x: pg.Surface((20, 10)))
        settings_manager = example_settings_manager
        settings_manager._load_images()

        assert len(settings_manager.settings["images"]["images"]) == len(
            example_settings_dict_with_tuples["images"]["sources"]
        )

    def test_load_images_file_not_found_error_not_raised(
        self, example_settings_manager: SettingsManager
    ) -> None:
        """`FileNotFoundError` not raised further when image files are not found."""
        settings_manager = example_settings_manager
        try:
            settings_manager._load_images()
        except FileNotFoundError as error:
            assert False, f"{error}"

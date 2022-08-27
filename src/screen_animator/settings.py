from pathlib import Path
import random
import logging
import pygame as pg

try:
    import tomlib
except ModuleNotFoundError:
    import tomli as tomlib

log = logging.getLogger(__name__)


class SettingsImporter:
    """
    Imports settings from a TOML file and validates, ready for further use.

    Methods
    -------
    import_settings
        Imports the settings from specified file and validates imported values.
    """

    def __init__(self):
        """Initialise the importer. Nothing much is done at this stage."""
        self._settings = None

    def import_settings(self, settings_file: str | Path) -> dict:
        """
        Imports the settings from the specified file, validates, and stores and returns a dictionary.

        Parameters
        ----------
        settings_file
            Path to the TOML file containing settings.

        Returns
        -------
        dict
            The imported and validated settings.
        """

        settings_path = Path(settings_file)
        self._read_settings(settings_path)
        self._validate_settings()
        self._settings = self._convert_colors_to_tuples(self._settings)

        return self._settings

    def _read_settings(self, settings_path: Path) -> None:
        with settings_path.open("rb") as file:
            self._settings = tomlib.load(file)

    def _validate_settings(self) -> None:
        match self._settings:
            case {
                "colors": list(),
                "messages": {
                    "messages": list() | str(),
                    "separator": str(),
                    "typeface": str(),
                    "size": int(),
                    "bold": bool(),
                    "italic": bool(),
                    "anti-aliasing": bool(),
                    "scroll_speed": float() | int(),
                    "outline_width": int(),
                    "outline_colors": list(),
                },
                "images": {
                    "sources": list() | str(),
                    "number": int(),
                },
                "timings": {
                    "fps": int(),
                    "image_change_time": int(),
                    "color_change_time": int(),
                },
            }:
                pass
            case _:
                raise ValueError(f"Invalid configuration {self._settings}")

    def _convert_colors_to_tuples(self, input_item):
        match input_item:
            case [int(), int(), int()]:
                return tuple(input_item)
            case list():
                return [self._convert_colors_to_tuples(item) for item in input_item]
            case dict():
                return {
                    key: self._convert_colors_to_tuples(value)
                    for key, value in input_item.items()
                }
            case _:
                return input_item


class SettingsManager:
    """
    Reads in settings, manipulates, and provides provisions for generating dynamic settings.

    Methods
    -------
    set_colors
        Randomly set the background, text, and text outline color.
    """

    def __init__(self, importer: SettingsImporter, settings_file: str | Path) -> None:
        """
        Initialise by using a settings importer to imported a specified file, then setting up some initial settings.

        Parameters
        ----------
        importer
            Low-level importer for reading and validating settings file.
        settings_file
            Path to settings file.
        """

        self._importer = importer
        self._settings = self._import_settings(settings_file)
        self._setup_settings()

    @property
    def settings(self) -> dict:
        """Dictionary of all settings."""
        return self._settings

    def set_colors(self) -> None:
        """Set background, text, and text outline colors from the available options in the settings provided."""

        if self._settings.get("bg") is None:
            self._settings["bg"] = {}
        self._settings["bg"]["color"] = random.choice(self._settings["colors"])

        self._settings["messages"]["color"] = random.choice(self._settings["colors"])
        while self._settings["messages"]["color"] == self._settings["bg"]["color"]:
            self._settings["messages"]["color"] = random.choice(
                self._settings["colors"]
            )

        self.settings["messages"]["outline_color"] = random.choice(
            self._settings["messages"]["outline_colors"]
        )

    def _import_settings(self, settings_file: str | Path) -> dict:
        return self._importer.import_settings(settings_file)

    def _setup_settings(self):
        self.set_colors()
        self._set_font()
        self._settings["messages"]["message"] = self._generate_message
        self._load_images()

    def _set_font(self) -> None:
        messages_dict = self._settings["messages"]
        messages_dict["font"] = pg.font.SysFont(
            messages_dict["typeface"],
            messages_dict["size"],
            bold=messages_dict["bold"],
            italic=messages_dict["italic"],
        )

    def _generate_message_text(self) -> str:
        messages_dict = self._settings["messages"]

        return f"{random.choice(messages_dict['messages'])}{messages_dict['separator']}"

    def _generate_message(self) -> pg.Surface:
        messages_dict = self._settings["messages"]

        return messages_dict["font"].render(
            self._generate_message_text(),
            messages_dict["anti-aliasing"],
            messages_dict["color"],
        )

    def _load_images(self):
        images_dict = self._settings["images"]
        if len(images_dict["sources"]) >= 1:
            images_dict["images"] = []
            for image in images_dict["sources"]:
                try:
                    images_dict["images"].append(pg.image.load(image))
                except FileNotFoundError:
                    log.exception("%s not found", image)

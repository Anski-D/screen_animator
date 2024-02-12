from pathlib import Path
import random
import logging

import pygame as pg

from .image_loading import ImageLoader

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

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

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    def import_settings(self, settings_file: str | Path) -> dict:
        """
        Imports the settings from the specified file, validates, and stores and
        returns a dictionary.

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
        log.info("Converting certain lists to tuples")
        self._settings = self._convert_colors_to_tuples(self._settings)

        return self._settings

    def _read_settings(self, settings_path: Path) -> None:
        log.info("Reading settings from %s...", settings_path)
        with settings_path.open("rb") as file:
            self._settings = tomllib.load(file)

    def _validate_settings(self) -> None:
        log.info("Validating input file matches expected format")
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
                    "scroll_speed": int(),
                    "outline_width": int(),
                    "outline_copies": int(),
                    "outline_colors": list(),
                },
                "images": {
                    "sources": list() | str(),
                    "number": int(),
                    "reposition_attempts": int(),
                },
                "timings": {
                    "fps": int() | float(),
                    "image_change_time": int() | float(),
                    "color_change_time": int() | float(),
                },
            }:
                log.info("Validation successful")
            case _:
                raise ValueError(f"Invalid configuration {self._settings}")

    def _convert_colors_to_tuples(self, input_item):
        match input_item:
            case [int(), int(), int()] | [str(), int()]:
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
        Initialise by using a settings importer to import a specified file,
        then setting up some initial settings.

        Parameters
        ----------
        importer
            Low-level importer for reading and validating settings file.
        settings_file
            Path to settings file.
        """
        self._importer = importer
        self._settings_file = settings_file
        self._settings = self._import_settings(self._settings_file)
        self._setup_settings()

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._importer}, {self._settings_file})"

    @property
    def settings(self) -> dict:
        """Dictionary of all settings."""
        return self._settings

    def set_colors(self) -> None:
        """Set background, text, and text outline colors from the available options
        in the settings provided."""
        if self._settings.get("bg") is None:
            self._settings["bg"] = {}
        self._settings["bg"]["color"] = random.choice(self._settings["colors"])
        log.debug("Set background color as: %s", self._settings["bg"]["color"])

        messages_dict = self._settings["messages"]
        messages_dict["color"] = random.choice(self._settings["colors"])
        while messages_dict["color"] == self._settings["bg"]["color"]:
            messages_dict["color"] = random.choice(self._settings["colors"])
        log.debug("Set text color as: %s", messages_dict["color"])

        match messages_dict["outline_colors"]:
            case (int(), int(), int()) as outline_color:
                pass
            case outline_colors:
                outline_color = random.choice(outline_colors)
        messages_dict["outline_color"] = outline_color
        log.debug("Set outline color as: %s", messages_dict["outline_color"])

    def generate_message_text(self) -> str:
        """
        Get a message from the available options.

        Returns
        -------
        str
            The selected message.
        """
        messages_dict = self._settings["messages"]

        return f"{random.choice(messages_dict['messages'])}{messages_dict['separator']}"

    def _import_settings(self, settings_file: str | Path) -> dict:
        return self._importer.import_settings(settings_file)

    def _setup_settings(self):
        self.set_colors()
        self._set_font()
        self._load_images()
        self._settings["timings"]["fps_actual"] = self._settings["timings"]["fps"]

    def _set_font(self) -> None:
        log.info("Setting `pygame` font for text rendering")
        messages_dict = self._settings["messages"]
        messages_dict["font"] = pg.font.SysFont(
            messages_dict["typeface"],
            messages_dict["size"],
            bold=messages_dict["bold"],
            italic=messages_dict["italic"],
        )

    def _load_images(self):
        images_dict = self._settings["images"]
        if len(images_dict["sources"]) >= 1:
            log.info("Loading and scaling images for rendering")
            images_dict["images"] = []
            image_loader = ImageLoader()
            for image_src, width in images_dict["sources"]:
                image = image_loader.load_image(image_src, width)
                if image is not None:
                    images_dict["images"].append(image)

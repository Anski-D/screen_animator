from pathlib import Path
import random
import pygame as pg
try:
    import tomlib
except ModuleNotFoundError:
    import tomli as tomlib


class SettingsImporter:
    """

    """
    def __init__(self):
        """

        """
        self._settings = None

    def import_settings(self, settings_file: str | Path) -> dict:
        """

        Parameters
        ----------
        settings_file

        Returns
        -------

        """
        settings_path = Path(settings_file)
        self._read_settings(settings_path)
        self._validate_settings()

        return self._settings

    def _read_settings(self, settings_path: Path) -> None:
        with settings_path.open("rb") as file:
            self._settings = tomlib.load(file)

    def _validate_settings(self) -> None:
        match self._settings:
            case {
                "colours": list(),
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
                    "outline_colours": list(),
                },
                "images": {
                    "sources": list() | str(),
                    "number": int(),
                },
                "timings": {
                    "fps": int(),
                    "image_change_time": int(),
                    "colour_change_time": int(),
                }
            }:
                pass
            case _:
                raise ValueError(f"Invalid configuration {self._settings}")


class SettingsManager:
    def __init__(self, importer: SettingsImporter, settings_file: str | Path) -> None:
        self._importer = importer
        self._settings = self._import_settings(settings_file)
        self._setup_settings()

    @property
    def settings(self) -> dict:
        """

        Returns
        -------

        """
        return self._settings

    def set_colours(self) -> None:
        """

        Returns
        -------

        """
        if self._settings.get('bg') is None:
            self._settings['bg'] = {}
        self._settings['bg']['colour'] = random.choice(self._settings['colours'])

        self._settings['messages']['colour'] = random.choice(self._settings['colours'])
        while self._settings['messages']['colour'] == self._settings['bg']['colour']:
            self._settings['messages']['colour'] = random.choice(self._settings['colours'])

        self.settings['messages']['outline_colour'] = \
            random.choice(self._settings['messages']['outline_colours'])

    def _import_settings(self, settings_file: str | Path) -> dict:
        return self._importer.import_settings(settings_file)

    def _setup_settings(self):
        self.set_colours()
        self._set_font()
        self._settings['messages']['message'] = self._generate_message
        self._load_images()

    def _set_font(self) -> None:
        messages_dict = self._settings['messages']
        messages_dict['font'] = pg.font.SysFont(
            messages_dict['typeface'],
            messages_dict['size'],
            bold=messages_dict['bold'],
            italic=messages_dict['italic'],
        )

    def _generate_message_text(self) -> str:
        messages_dict = self._settings['messages']

        return f"{random.choice(messages_dict['messages'])}{messages_dict['separator']}"

    def _generate_message(self) -> pg.Surface:
        messages_dict = self._settings['messages']

        return messages_dict['font'].render(
            self._generate_message_text(),
            messages_dict['anti-aliasing'],
            messages_dict['colour'],
        )

    def _load_images(self):
        images_dict = self._settings['images']
        if len(images_dict['sources']) >= 1:
            images_dict['images'] = []
            for image in images_dict['sources']:
                try:
                    images_dict['images'].append(pg.image.load(image))
                except FileNotFoundError as error:
                    print(error)

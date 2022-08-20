from pathlib import Path
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

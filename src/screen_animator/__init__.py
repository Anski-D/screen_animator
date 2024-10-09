import importlib.resources
import shutil
from functools import partial
import argparse

import example
from screen_animator.controller import Controller
from screen_animator.item_groups import (
    ItemGroup,
    TimedItemGroup,
    LeftScrollingTextItemGroup,
    ColorChangeItemGroup,
    RandomImagesItemGroup,
    FpsCounterItemGroup,
)
from screen_animator.image_loading import ImageLoader, SvgTypeImageLoader
from screen_animator.model import Model
from screen_animator.settings import SettingsManager
from screen_animator.log_setup import setup_logging
from screen_animator.sa import ScreenAnimator

EXAMPLE_FILES = ["inputs.toml"]


def copy_examples() -> None:
    """Copies example files to working directory."""
    for file in EXAMPLE_FILES:
        example_path = importlib.resources.path(example, file)
        with example_path as path:
            shutil.copy2(path, path.name)


def parse_args() -> argparse.Namespace:
    """Processes the command line arguments provided."""
    parser = argparse.ArgumentParser(
        prog="ScreenAnimator",
        description="A Python app to generate animated messages and images on a screen, with a focus on the Raspberry Pi.",
    )
    parser.add_argument(
        "-i",
        "--input",
        default="inputs.toml",
        help="path to TOML file with inputs (optional, falls back to `inputs.toml` by default)",
    )
    parser.add_argument(
        "-r",
        "--rotate",
        action="store_true",
        help="rotate rendered output by 180 degrees (optional, disabled by default)",
    )
    parser.add_argument(
        "-f",
        "--fps",
        action="store_true",
        help="turn on FPS counter (optional, off by default, forced on if debug mode used)",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="turns on debug mode which limits output to windowed mode, increases logging, and renders FPS counter (optional, off by default)",
    )
    parser.add_argument(
        "-l",
        "--logging",
        default="",
        help="activates logging and sets logging level (off by default, writes to log file when on)",
    )

    return parser.parse_args()


def main() -> None:
    """Main app function to run."""
    ImageLoader.register_loader(".svg", SvgTypeImageLoader)

    groups = [
        partial(TimedItemGroup, wrapped_group=ColorChangeItemGroup),
        partial(TimedItemGroup, wrapped_group=RandomImagesItemGroup),
        LeftScrollingTextItemGroup,
    ]

    for group in groups:
        ScreenAnimator.register_item_group(group)  # type: ignore

    args = parse_args()
    setup_logging(args.logging)

    screen_animator = ScreenAnimator(
        input_file=args.input,
        rotated=args.rotate,
        fps_on=args.fps,
        debug=args.debug,
    )
    screen_animator.run()


if __name__ == "__main__":
    main()

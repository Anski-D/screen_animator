import logging
import random
from abc import ABC, abstractmethod

import pygame as pg
import numpy as np

from .items import ScrollingMovement, RandomMovement, Item
from .settings import SettingsManager

log = logging.getLogger(__name__)


class ItemGroup(ABC, pg.sprite.Group):
    """
    Interface for `Item` groups.

    Methods
    -------
    create
        Create items in group (sublasses to implement).
    update
        Update items in group (sublasses to implement).
    """

    def __init__(self, settings_manager: SettingsManager, perimeter: pg.Rect) -> None:
        """
        Initialise group with settings and context perimeter.

        Parameters
        ----------
        settings_manager
            Dictionary of settings.
        perimeter
            Outer limit of 'canvas' in `pygame`.
        """
        super().__init__()
        self._settings_manager = settings_manager
        self._settings = self._settings_manager.settings
        self._perimeter = perimeter
        log.info("Creating %s", self)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._settings_manager}, {self._perimeter})"

    @abstractmethod
    def create(self) -> None:
        """Create item(s) in group, to be implemented by sublasses."""


class LeftScrollingTextGroup(ItemGroup):
    """
    Group of items that will scroll messages to the left.

    Methods
    -------
    create
        Create a message with a set speed to the left.
    update
        Update messages depending on message position.
    """

    _movement = ScrollingMovement

    def __init__(self, settings_manager: SettingsManager, perimeter: pg.Rect) -> None:
        """
        Initialize group with a settings manager and defined perimeter.

        Parameters
        ----------
        settings_manager
            Manages settings.
        perimeter
            Defines outer perimeter.
        """
        super().__init__(settings_manager, perimeter)

        speed = (
            self._settings["messages"]["scroll_speed"]
            // self._settings["timings"]["fps"]
        )
        self._scrolling_movement = self._movement(speed, "left")

    def create(self) -> None:
        """
        Create a message `Item` that scrolls to the left with a set speed.

        Message is initially placed with middle-left set at the middle-right of the
        perimeter, i.e. off-screen to the right.
        """
        messages_dict = self._settings["messages"]
        self._settings_manager.set_font()
        message_text = self._settings_manager.generate_message_text()
        log.debug("Creating %s with text: %s", Item.__name__, message_text)
        start_position = self._calculate_start_position(message_text)
        self._set_outline(message_text, start_position)
        message = Item(
            self,
            self._generate_message(message_text, messages_dict["font"]),
            self._perimeter,
            self._scrolling_movement,
        )
        setattr(message, "message_text", message_text)
        setattr(message, "font", messages_dict["font"])
        message.rect.midleft = start_position
        message.rect.x += messages_dict["outline_width"]

    def update(self):
        """
        Update messages in group.

        If the message has left the left side of the perimeter entirely, it will be
        deleted. If all messages are within the right-hand perimeter, a new message
        will be generated.
        """
        self._set_speed()
        super().update()

        for message in self.sprites():
            if message.rect.right < self._perimeter.left:
                log.debug("%s has scrolled off screen, destroying", message)
                message.kill()
            else:
                try:
                    message.content = self._generate_message(
                        getattr(message, "message_text"),
                        getattr(message, "font"),
                    )
                except AttributeError:
                    pass

        if all(
            message.rect.right <= self._perimeter.right for message in self.sprites()
        ):
            self.create()

    def _generate_message(self, message_text: str, font: pg.Font) -> pg.Surface:
        messages_dict = self._settings["messages"]

        return font.render(
            message_text,
            messages_dict["anti-aliasing"],
            messages_dict["color"],
        )

    def _set_outline(self, message_text: str, start_position: tuple[int, int]) -> None:
        messages_dict = self._settings["messages"]
        log.debug("Setting text outline with width %s", messages_dict["outline_width"])
        outline_width = messages_dict["outline_width"]
        if outline_width > 0:
            outline_text = messages_dict["font"].render(
                message_text,
                messages_dict["anti-aliasing"],
                messages_dict["outline_color"],
            )
            angles = np.linspace(
                0, 360, messages_dict["outline_copies"], endpoint=False
            )
            x_shift = outline_width * np.cos(np.radians(angles - 90)) + outline_width
            y_shift = outline_width * np.sin(np.radians(angles - 90))
            xy_shifts = np.transpose(np.vstack((x_shift, y_shift)))
            for xy_shift in xy_shifts:
                outline = Item(
                    self, outline_text, self._perimeter, self._scrolling_movement
                )
                outline.rect.midleft = start_position
                outline.rect.x += xy_shift[0]
                outline.rect.y += xy_shift[1]

    def _set_speed(self) -> None:
        fps_actual = self._settings["timings"]["fps_actual"]
        if fps_actual > 0:
            speed = self._settings["messages"]["scroll_speed"] / fps_actual
            self._scrolling_movement.speed = speed

    def _calculate_start_position(self, message_text: str) -> tuple[int, int]:
        messages_dict = self._settings["messages"]
        if not messages_dict["start_middle"]:
            dummy_message = self._generate_message(message_text, messages_dict["font"])
            height = dummy_message.get_height()

            return (
                self._perimeter.right,
                random.randint(
                    height // 2,
                    self._perimeter.bottom - height // 2,
                ),
            )

        return self._perimeter.midright


class RandomImagesGroup(ItemGroup):
    """
    Group of items that will remove randomly within the specified perimeter.

    Methods
    -------
    create
        Create all the image items.
    update
        Update the position of all image items.
    """

    _movement = RandomMovement

    def create(self) -> None:
        """Create all the image items, set to move randomly within the perimeter."""
        image_settings = self._settings["images"]
        movement = self._movement()
        for _ in range(image_settings["number"]):
            for image in image_settings["images"]:
                log.debug("Creating `pygame` image: %s", image)
                Item(self, image, self._perimeter, movement)

    def update(self):
        """
        Update the position, randomly, of all the images in the group.

        Image position is updated sequentially, and each is compared to the position
        of newly positioned images to ensure no collisions.
        """
        log.debug("Repositioning all images")
        group = []
        reattempts_taken_total = 0
        num_items = len(self.sprites())
        for image_idx, image in enumerate(self.sprites(), 1):
            self.remove(image)
            image.update()
            reattempts_allowed = self._settings["images"]["reposition_attempts"]
            while (
                pg.sprite.spritecollideany(image, group) and abs(reattempts_allowed) > 0
            ):
                image.update()
                reattempts_allowed -= 1
                reattempts_taken_total += 1
                if reattempts_taken_total % 100000 == 0:
                    log.debug(
                        "%s reattempts so far, currently on image %s of %s",
                        reattempts_taken_total,
                        image_idx,
                        num_items,
                    )
            group.append(image)
        log.debug(
            "All images (%s total) repositioned with %s total reattempts",
            num_items,
            reattempts_taken_total,
        )
        self.add(group)


class ColorChangeGroup(ItemGroup):
    """
    Manages when colors are changed.

    Methods
    -------
    create
        Set the initial time tracked by `pygame`.
    update
        Change colors if time threshold reached.
    """

    _time: int

    def create(self) -> None:
        """Set the elapsed time according to `pygame`."""
        self._time = pg.time.get_ticks()

    def update(self):
        """Check elapsed time, update colors if sufficient time has passed."""
        time = pg.time.get_ticks()
        time_diff = time - self._time
        if time_diff >= self._settings["timings"]["color_change_time"] * 1000:
            log.debug("%s milliseconds passed, updating colors", time_diff)
            self._settings_manager.set_colors()
            self._time = time


class TimedRandomImagesGroup(ItemGroup):
    """
    Wraps a RandomImagesGroup and restricts updates to defined elapsed time threshold.

    Methods
    -------
    create
        Initialize a group with randomly moving images, set initial time.
    update
        Update wrapped group if time threshold reached.
    """

    _wrapped_group_type = RandomImagesGroup
    _time: int

    def __init__(self, settings_manager: SettingsManager, perimeter: pg.Rect) -> None:
        """
        Initialize the group with a settings manager and outer perimeter.

        Parameters
        ----------
        settings_manager
            Manages settings.
        perimeter
            Defines outer perimeter.
        """
        super().__init__(settings_manager, perimeter)

        self._wrapped_group = self._wrapped_group_type(settings_manager, perimeter)

    def sprites(self):
        return self._wrapped_group.sprites()

    def create(self) -> None:
        """Create the wrapped group of random moving images."""
        self._wrapped_group.create()
        self._time = pg.time.get_ticks()

    def update(self):
        """Update item positions if time threshold met."""
        time = pg.time.get_ticks()
        time_diff = time - self._time
        if time_diff >= self._settings["timings"]["image_change_time"] * 1000:
            log.debug("%s milliseconds passed, updating image positions", time_diff)
            self._wrapped_group.update()
            self._time = time


class FpsCounterGroup(ItemGroup):
    """
    Counter for fps.

    Methods
    -------
    create
        Create the fps counter.
    update
        Update the fps counter.
    """

    def create(self) -> None:
        """Create the fps counter."""
        messages_dict = self._settings["messages"]
        fps_font = pg.font.SysFont(messages_dict["typeface"], 36)
        fps_actual = self._settings["timings"]["fps_actual"]
        text = f"{fps_actual:.2f}"
        content = fps_font.render(text, messages_dict["anti-aliasing"], (0, 0, 0))
        fps = Item(self, content, self._perimeter)
        fps.rect.x = 10
        fps.rect.y = 10

    def update(self):
        """Update the fps counter."""
        self.empty()
        self.create()

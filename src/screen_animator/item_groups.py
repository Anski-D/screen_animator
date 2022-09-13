from abc import ABC, abstractmethod
import pygame as pg
from .items import ScrollingMovement, RandomMovement, Item
from .settings import SettingsManager


class ItemGroup(ABC):
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
        self._settings_manager = settings_manager
        self._settings = self._settings_manager.settings
        self._perimeter = perimeter
        self._group = pg.sprite.Group()

    @property
    def items(self) -> list[Item]:
        """List of items in group."""
        return self._group.sprites()

    @abstractmethod
    def create(self) -> None:
        """Create item(s) in group, to be implemented by sublasses."""

    @abstractmethod
    def update(self) -> None:
        """Update item(s) in group, to be implemented by sublasses."""


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
        super().__init__(settings_manager, perimeter)

        speed = (
            self._settings["messages"]["scroll_speed"]
            / self._settings["timings"]["fps"]
        )
        self._scrolling_movement = self._movement(speed, "left")

    def create(self) -> None:
        """
        Create a message `Item` that scrolls to the left with a set speed.

        Message is initially placed with middle-left set at the middle-right of the
        perimeter, i.e. off-screen to the right.
        """
        message_text = self._settings_manager.generate_message_text()
        message = Item(
            self._group,
            self._generate_message(message_text),
            self._perimeter,
            self._scrolling_movement,
        )
        setattr(message, "message_text", message_text)
        message.rect.midleft = self._perimeter.midright

    def update(self) -> None:
        """
        Update messages in group.

        If the message has left the left side of the perimeter entirely, it will be
        deleted. If all messages are within the right-hand perimeter, a new message
        will be generated.
        """
        self._group.update()

        for message in self.items:
            if message.rect.right < self._perimeter.left:
                message.kill()
            else:
                message.content = self._generate_message(
                    getattr(message, "message_text")
                )

        if all(message.rect.right <= self._perimeter.right for message in self.items):
            self.create()

    def _generate_message(self, message_text: str) -> pg.Surface:
        messages_dict = self._settings["messages"]

        return messages_dict["font"].render(
            message_text,
            messages_dict["anti-aliasing"],
            messages_dict["color"],
        )


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
                Item(self._group, image, self._perimeter, movement)

    def update(self) -> None:
        """
        Update the position, randomly, of all the images in the group.

        Image position is updated sequentially, and each is compared to the position
        of newly positioned images to ensure no collisions.
        """
        group = pg.sprite.Group()
        for image in self.items:
            self._group.remove(image)
            image.update()
            while pg.sprite.spritecollideany(image, group):
                image.update()
            group.add(image)
        self._group = group


class ColorChangeGroup(ItemGroup):
    _time: int

    def create(self) -> None:
        self._time = pg.time.get_ticks()

    def update(self) -> None:
        time = pg.time.get_ticks()
        if time - self._time >= self._settings["timings"]["color_change_time"] * 1000:
            self._settings_manager.set_colors()
            self._time = time


class TimedRandomImagesGroup(ItemGroup):
    _wrapped_group_type = RandomImagesGroup
    _time: int

    def __init__(self, settings_manager: SettingsManager, perimeter: pg.Rect) -> None:
        super().__init__(settings_manager, perimeter)

        self._wrapped_group = self._wrapped_group_type(settings_manager, perimeter)

    @property
    def items(self) -> list[Item]:
        return self._wrapped_group.items

    def create(self) -> None:
        self._wrapped_group.create()
        self._time = pg.time.get_ticks()

    def update(self) -> None:
        time = pg.time.get_ticks()
        if time - self._time >= self._settings["timings"]["image_change_time"] * 1000:
            self._wrapped_group.update()
            self._time = time


class FpsCounterGroup(ItemGroup):
    def __init__(self, settings_manager: SettingsManager, perimeter: pg.Rect) -> None:
        super().__init__(settings_manager, perimeter)

        self._clock = pg.time.Clock()

    def create(self) -> None:
        self._group = pg.sprite.Group()
        messages_dict = self._settings["messages"]
        fps_font = pg.font.SysFont(messages_dict["typeface"], 36)
        self._clock.tick()
        text = f"{self._clock.get_fps():.2f}"
        content = fps_font.render(text, messages_dict["anti-aliasing"], (0, 0, 0))
        fps = Item(self._group, content, self._perimeter)
        fps.rect.x = 10
        fps.rect.y = 10

    def update(self) -> None:
        self.create()

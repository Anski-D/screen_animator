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
        self._set_outline(message_text)
        message = Item(
            self._group,
            self._generate_message(message_text),
            self._perimeter,
            self._scrolling_movement,
        )
        setattr(message, "message_text", message_text)
        message.rect.midleft = self._perimeter.midright
        message.rect.x += self._settings["messages"]["outline_width"]

    def update(self) -> None:
        """
        Update messages in group.

        If the message has left the left side of the perimeter entirely, it will be
        deleted. If all messages are within the right-hand perimeter, a new message
        will be generated.
        """
        self._set_speed()
        self._group.update()

        for message in self.items:
            if message.rect.right < self._perimeter.left:
                message.kill()
            else:
                try:
                    message.content = self._generate_message(
                        getattr(message, "message_text")
                    )
                except AttributeError:
                    pass

        if all(message.rect.right <= self._perimeter.right for message in self.items):
            self.create()

    def _generate_message(self, message_text: str) -> pg.Surface:
        messages_dict = self._settings["messages"]

        return messages_dict["font"].render(
            message_text,
            messages_dict["anti-aliasing"],
            messages_dict["color"],
        )

    def _set_outline(self, message_text: str) -> None:
        messages_dict = self._settings["messages"]
        outline_width = messages_dict["outline_width"]
        if outline_width > 0:
            outline_text = messages_dict["font"].render(
                message_text,
                messages_dict["anti-aliasing"],
                messages_dict["outline_color"],
            )

            outline1 = Item(
                self._group, outline_text, self._perimeter, self._scrolling_movement
            )
            outline1.rect.midleft = self._perimeter.midright
            outline1.rect.x += outline_width
            outline1.rect.y -= outline_width

            outline2 = Item(
                self._group, outline_text, self._perimeter, self._scrolling_movement
            )
            outline2.rect.midleft = self._perimeter.midright
            outline2.rect.x += 2 * outline_width
            outline2.rect.y -= outline_width

            outline3 = Item(
                self._group, outline_text, self._perimeter, self._scrolling_movement
            )
            outline3.rect.midleft = self._perimeter.midright
            outline3.rect.x += 2 * outline_width

            outline4 = Item(
                self._group, outline_text, self._perimeter, self._scrolling_movement
            )
            outline4.rect.midleft = self._perimeter.midright
            outline4.rect.x += 2 * outline_width
            outline4.rect.y += outline_width

            outline5 = Item(
                self._group, outline_text, self._perimeter, self._scrolling_movement
            )
            outline5.rect.midleft = self._perimeter.midright
            outline5.rect.x += outline_width
            outline5.rect.y += outline_width

            outline6 = Item(
                self._group, outline_text, self._perimeter, self._scrolling_movement
            )
            outline6.rect.midleft = self._perimeter.midright
            outline6.rect.y += outline_width

            outline7 = Item(
                self._group, outline_text, self._perimeter, self._scrolling_movement
            )
            outline7.rect.midleft = self._perimeter.midright

            outline8 = Item(
                self._group, outline_text, self._perimeter, self._scrolling_movement
            )
            outline8.rect.midleft = self._perimeter.midright
            outline8.rect.y -= outline_width

    def _set_speed(self) -> None:
        fps_actual = self._settings["timings"]["fps_actual"]
        if fps_actual > 0:
            speed = self._settings["messages"]["scroll_speed"] / fps_actual
            self._scrolling_movement.speed = speed


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
            attempts = self._settings["images"]["reposition_attempts"]
            while pg.sprite.spritecollideany(image, group) and abs(attempts) > 0:
                attempts -= 1
                image.update()
            group.add(image)
        self._group = group


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

    def update(self) -> None:
        """Check elapsed time, update colors if sufficient time has passed."""
        time = pg.time.get_ticks()
        if time - self._time >= self._settings["timings"]["color_change_time"] * 1000:
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

    @property
    def items(self) -> list[Item]:
        """Constituent items of group."""
        return self._wrapped_group.items

    def create(self) -> None:
        """Create the wrapped group of random moving images."""
        self._wrapped_group.create()
        self._time = pg.time.get_ticks()

    def update(self) -> None:
        """Update item positions if time threshold met."""
        time = pg.time.get_ticks()
        if time - self._time >= self._settings["timings"]["image_change_time"] * 1000:
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
        self._group = pg.sprite.Group()
        messages_dict = self._settings["messages"]
        fps_font = pg.font.SysFont(messages_dict["typeface"], 36)
        fps_actual = self._settings["timings"]["fps_actual"]
        text = f"{fps_actual:.2f}"
        content = fps_font.render(text, messages_dict["anti-aliasing"], (0, 0, 0))
        fps = Item(self._group, content, self._perimeter)
        fps.rect.x = 10
        fps.rect.y = 10

    def update(self) -> None:
        """Update the fps counter."""
        self.create()

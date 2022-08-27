from abc import ABC, abstractmethod
import pygame as pg
from .items import ScrollingMovement, RandomMovement, Item


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

    def __init__(self, settings: dict, perimeter: pg.Rect) -> None:
        """
        Initialise group with settings and context perimeter.

        Parameters
        ----------
        settings
            Dictionary of settings.
        perimeter
            Outer limit of 'canvas' in `pygame`.
        """
        self._settings = settings
        self._perimeter = perimeter
        self._group = pg.sprite.Group()

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

    def create(self) -> None:
        """
        Create a message `Item` that scrolls to the left with a set speed.

        Message is initially placed with middle-left set at the middle-right of the perimeter,
        i.e. off-screen to the right.
        """
        speed = (
            self._settings["messages"]["scroll_speed"]
            / self._settings["timings"]["fps"]
        )
        movement = self._movement(speed, "left")
        message = Item(
            self._group,
            self._settings["messages"]["message"](),
            self._perimeter,
            movement,
        )
        message.rect.midleft = self._perimeter.midright

    def update(self) -> None:
        """
        Update messages in group.

        If the message has left the left side of the perimeter entirely, it will be deleted. If
        all messages are within the right-hand perimeter, a new message will be generated.
        """
        self._group.update()
        for message in self._group.sprites():
            if message.rect.right < self._perimeter.left:
                message.kill()
        if all(
            message.rect.right <= self._perimeter.right
            for message in self._group.sprites()
        ):
            self.create()


class RandomImagesGroup(ItemGroup):
    _movement = RandomMovement

    def create(self) -> None:
        image_settings = self._settings["images"]
        for _ in range(image_settings["number"]):
            for image in image_settings["images"]:
                movement = self._movement()
                Item(self._group, image, self._perimeter, movement)

    def update(self) -> None:
        group = pg.sprite.Group()
        for image in self._group.sprites():
            self._group.remove(image)
            image.update()
            while pg.sprite.spritecollideany(image, group):
                image.update()
            group.add(image)
        self._group = group

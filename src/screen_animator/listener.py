from abc import ABC, abstractmethod


class Listener(ABC):
    """
    Inheriting classes can be notified of changes they are listening for.

    Methods
    -------
    notify
        Do something when notified, to be implemented by subclasses.
    """

    @abstractmethod
    def notify(self) -> None:
        """Subclasses should implement behavior for when notified."""

from abc import ABC, abstractmethod
from weakref import WeakKeyDictionary


class Observer(ABC):
    """
    Inheriting classes can be notified of changes they are watching for.

    Methods
    -------
    notify
        Do something when notified, to be implemented by subclasses.
    """

    @abstractmethod
    def notify(self) -> None:
        """Subclasses should implement behavior for when notified."""


class Observable(ABC):
    """
    Inheriting classes can be watched and send out notifications.

    Methods
    -------
    add_observer
        Add an observer.
    notify_observers
        Notify all observers that a change has occured.
    remove_observers
        Remove specified observer.
    """

    def __init__(self) -> None:
        """Create a dictionary with weak keys for storing observers."""
        self._observers = WeakKeyDictionary()

    def add_observer(self, observer: Observer) -> None:
        """
        Add an observer.

        Parameters
        ----------
        observer
            Observer to be registered.
        """
        self._observers[observer] = 1

    def notify_observers(self) -> None:
        """Notify all observers of a change."""
        for observer in self._observers.keys():
            observer.notify()

    def remove_observer(self, observer: Observer) -> None:
        """
        Remove specified observer from being notified of any further changes.

        Parameters
        ----------
        observer
            Observer to be removed.
        """
        if observer in self._observers.keys():
            del self._observers[observer]

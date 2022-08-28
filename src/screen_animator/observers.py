from abc import ABC
from weakref import WeakKeyDictionary


class Observer(ABC):
    def notify(self):
        pass


class Observable(ABC):
    def __init__(self):
        self._observers = WeakKeyDictionary()

    def add_observer(self, observer: Observer):
        self._observers[observer] = 1

    def notify_observer(self):
        for observer in self._observers.keys():
            observer.notify()

    def remove_observer(self, observer: Observer):
        if observer in self._observers.keys():
            del self._observers[observer]

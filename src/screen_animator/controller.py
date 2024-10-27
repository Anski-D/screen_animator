import logging
from collections.abc import Iterable

import pygame as pg

from screen_animator.listener import Listener
from screen_animator.model import Model

log = logging.getLogger(__name__)


class Controller:
    """
    Allows manipulation of the `screen_animator` model.

    Methods
    -------
    run
        Run model.
    quit
        Stop running.
    """

    def __init__(self, settings: dict, model: Model) -> None:
        """
        Set initial parameters.

        Parameters
        ----------
        settings
            Dictionary of settings.
        model
            The model to manipulate.
        """
        self._settings = settings
        self._model = model
        log.info("Creating %s", self)

        self._clock = pg.time.Clock()

        self._initialized = True

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self._settings},"
            f" {self._model},"
        )

    def run(self, event_manager: "EventManager") -> None:
        """Run `screen_animator` if view and model are ready."""
        log.info(
            "!!! %s%s !!!",
            type(self).__name__,
            " now running, entering main loop".upper(),
        )
        timings_dict = self._settings["timings"]
        while self._initialized:
            self._clock.tick(timings_dict["fps"])
            self._model.update()
            event_manager.manage_events()
            timings_dict["fps_actual"] = self._clock.get_fps()

        log.info("Run method complete, %s stopping", type(self).__name__)

    def quit(self) -> None:
        """Stop instance from continuing to run."""
        log.info("Telling %s to quit", type(self).__name__)
        self._initialized = False


class EventManager:
    """
    Manages events and handles events.

    Methods
    -------
    register_listener
        Register a listener for events.
    remove_listener
        Remove a listener for events.
    manage_events
        Manage all events.
    """
    _listeners: dict[tuple[int, ...], Listener]

    def __init__(self, listeners: Iterable[Listener] | None = None, event_types: Iterable[tuple[int, ...] | int] | None = None) -> None:
        """Store `Listener`s with `event_type` key."""
        self._listeners = {}
        if not (listeners is None or event_types is None):
            for listener, event_type in zip(listeners, event_types):
                self.register_listener(listener, event_type)

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    def register_listener(self, listener: Listener, event_type: tuple[int, ...] | int) -> None:
        """
        Add a listener.

        Parameters
        ----------
        listener
            Instance to be notified when event type found in queue.
        event_type
            Event type to be associated with listener.
        """
        event_type = (event_type,) if isinstance(event_type, int) else event_type
        log.info(
            "Adding listener `%s` to listeners for event type `%s`",
            listener,
            event_type,
        )
        self._listeners[event_type] = listener

    def remove_listener(self, event_type: tuple[int, ...] | int) -> None:
        """
        Remove specified listener from being notified of any further changes.

        Parameters
        ----------
        event_type
            Listener to be removed.
        """
        event_type = (event_type,) if isinstance(event_type, int) else event_type
        log.info("Removing listener `%s` from observers", event_type)
        if event_type in self._listeners:
            del self._listeners[event_type]

    def manage_events(self) -> None:
        """Process `pygame` queue of events for events of interest."""
        for event in pg.event.get():
            keys = tuple(key for key in (event.type, event.dict.get("key")) if key is not None)
            listener = self._listeners.get(keys)

            if listener is not None:
                listener.notify()


class QuitEvent(Listener):
    """
    Custom listener for quit events.

    Methods
    -------
    notify
        Tell associated class instances to quit.
    """

    def __init__(self, quitters: Iterable) -> None:
        """Store iterable of instances to quit when required."""
        self._quitters = quitters

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    def notify(self) -> None:
        """Iterate over instance to tell to quit."""
        for quitter in self._quitters:
            quitter.quit()

import logging
from enum import Enum, auto

from screen_animator.items import Speeder
from screen_animator.listener import Listener

log = logging.getLogger(__name__)


class Speed(Enum):
    MAINTAIN = auto()
    RESET = auto()
    FASTER = auto()
    SLOWER = auto()


class SpeedChanger:
    """
    Change speed of associated `Speeder` instances.

    Methods
    -------
    change_speed
        Change the speed according to provided speed change request.
    reset
        Reset speed to original value.
    increase
        Make the speed higher.
    decrease
        Make the speed lower.
    """

    _speed_change = 0.1

    def __init__(self, speeder: Speeder) -> None:
        """
        Set up instance with `Speeder` to manipulate.

        Parameters
        ----------
        speeder
            Instance of Speeder to manipulate.
        """
        self._speeder = speeder
        log.info("Creating %s", self)

        self._change_speed = {
            Speed.MAINTAIN: lambda: None,
            Speed.RESET: self.reset,
            Speed.FASTER: self.increase,
            Speed.SLOWER: self.decrease,
        }
        self._speed = self._speeder.speed

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._speeder})"

    def change_speed(self, speed_change: Speed) -> None:
        """
        Change the speed according to provided speed change request.

        Parameters
        ----------
        speed_change
            Speed change request.
        """
        self._change_speed.get(speed_change, self._change_speed[Speed.MAINTAIN])()

    def reset(self) -> None:
        """Reset speed to original value."""
        self._speeder.speed = self._speed

    def increase(self) -> None:
        """Make the speed higher."""
        self._speeder.speed += round(self._speed_change * self._speed)

    def decrease(self) -> None:
        """Make the speed lower."""
        self._speeder.speed -= round(self._speed_change * self._speed)
        self._speeder.speed = max(0.0, self._speeder.speed)


class SpeedAction(Listener):
    """
    Custom listener to carry out speed change actions.

    Methods
    -------
    notify
        Tell associated class instances to change speed.
    """

    _speed_action = Speed.MAINTAIN

    def __init__(self, speed_changer: SpeedChanger) -> None:
        """
        Store instance of `SpeedChanger` to manipulate.

        Parameters
        ----------
        speed_changer
            Instance of `SpeedChanger` to manipulate.
        """
        self._speed_changer = speed_changer
        log.info("Created %s", self)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._speed_changer})"

    def notify(self) -> None:
        """Change speed using `SpeedChanger` according to the provided action."""
        self._speed_changer.change_speed(self._speed_action)


class MaintainSpeedAction(SpeedAction):
    """`SpeedAction` that keeps speed as-is."""


class IncreaseSpeedAction(SpeedAction):
    """`SpeedAction` that increases speed."""

    _speed_action = Speed.FASTER


class DecreaseSpeedAction(SpeedAction):
    """`SpeedAction` that decreases speed."""

    _speed_action = Speed.SLOWER


class ResetSpeedAction(SpeedAction):
    """`SpeedAction` that resets speed."""

    _speed_action = Speed.RESET

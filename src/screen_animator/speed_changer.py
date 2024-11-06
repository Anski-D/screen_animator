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
    _speed_change = 0.1

    def __init__(self, speeder: Speeder) -> None:
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

    def reset(self) -> None:
        self._speeder.speed = self._speed

    def change_speed(self, speed_change: Speed) -> None:
        self._change_speed.get(speed_change, self._change_speed[Speed.MAINTAIN])()

    def increase(self) -> None:
        self._speeder.speed += int(self._speed_change * self._speed)

    def decrease(self) -> None:
        self._speeder.speed -= int(self._speed_change * self._speed)
        self._speeder.speed = max(0, self._speeder.speed)


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
        """Store instance of `SpeedChanger` to manipulate."""
        self._speed_changer = speed_changer
        log.info("Created %s", self)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._speed_changer})"

    def notify(self) -> None:
        """Change speed using `SpeedChanger` according to the provided action."""
        self._speed_changer.change_speed(self._speed_action)


class MaintainSpeedAction(SpeedAction):
    pass


class IncreaseSpeedAction(SpeedAction):
    _speed_action = Speed.FASTER


class DecreaseSpeedAction(SpeedAction):
    _speed_action = Speed.SLOWER


class ResetSpeedAction(SpeedAction):
    _speed_action = Speed.RESET

import pytest
import copy
from screen_animator.observers import Observer, Observable


@pytest.fixture
def example_observer() -> Observer:
    Observer.__abstractmethods__ = set()
    return Observer()


class TestObservable:
    def test_add_observer_values(self, example_observer: Observer) -> None:
        observable = Observable()
        observer = example_observer
        observable.add_observer(observer)

        assert observer in observable._observers.keys()

    def test_add_observer_same_len(self, example_observer: Observer) -> None:
        observable = Observable()
        observer = example_observer
        observable.add_observer(observer)
        observable.add_observer(observer)

        assert len(observable._observers) == 1

    def test_add_observer_multiple_len(self, example_observer: Observer) -> None:
        observable = Observable()
        observer1 = example_observer
        observable.add_observer(observer1)
        observer2 = copy.copy(observer1)
        observable.add_observer(observer2)

        assert len(observable._observers) == 2

    def test_weak_ref_len(self, example_observer: Observer) -> None:
        observable = Observable()
        observer1 = example_observer
        observable.add_observer(observer1)
        observer2 = copy.copy(observer1)
        observable.add_observer(observer2)
        observer3 = copy.copy(observer1)
        observable.add_observer(observer3)
        del observer2

        assert len(observable._observers) == 2

    def test_remove_observer(self, example_observer: Observer) -> None:
        observable = Observable()
        observer1 = example_observer
        observable.add_observer(observer1)
        observer2 = copy.copy(observer1)
        observable.add_observer(observer2)
        observer3 = copy.copy(observer1)
        observable.add_observer(observer3)
        observable.remove_observer(observer2)

        assert observer2 not in observable._observers.keys()

    def test_remove_observer_len(self, example_observer: Observer) -> None:
        observable = Observable()
        observer1 = example_observer
        observable.add_observer(observer1)
        observer2 = copy.copy(observer1)
        observable.add_observer(observer2)
        observer3 = copy.copy(observer1)
        observable.add_observer(observer3)
        observable.remove_observer(observer2)

        assert len(observable._observers) == 2

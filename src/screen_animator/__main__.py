from .model import Model
from .controller import Controller
from .settings import SettingsManager, SettingsImporter
from .item_groups import LeftScrollingTextGroup, RandomImagesGroup


def main():
    settings_manager = SettingsManager(SettingsImporter(), "../example_inputs/inputs.toml")

    item_groups = [LeftScrollingTextGroup, RandomImagesGroup]
    model = Model(settings_manager, item_groups)
    controller = Controller(settings_manager, model)


if __name__ == "__main__":
    main()

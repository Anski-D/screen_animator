import pygame as pg
from .model import Model
from .controller import Controller
from .settings import SettingsManager, SettingsImporter
from .item_groups import LeftScrollingTextGroup, ColorChangeGroup, TimedRandomImagesGroup


def main():
    pg.init()
    settings_manager = SettingsManager(SettingsImporter(), "../example_inputs/inputs.toml")
    item_groups = [LeftScrollingTextGroup, ColorChangeGroup, TimedRandomImagesGroup]
    model = Model(settings_manager, item_groups)
    controller = Controller(settings_manager, model)
    controller.init()
    controller.run()


if __name__ == "__main__":
    main()

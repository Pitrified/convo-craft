"""ConvoCraft project configuration."""

from loguru import logger as lg

from convo_craft.config.paths import ConvoCraftPaths
from convo_craft.meta.singleton import Singleton


class ConvoCraftConfig(metaclass=Singleton):
    """ConvoCraft project configuration."""

    def __init__(self) -> None:
        lg.info(f"Loading ConvoCraft config")
        self.paths = ConvoCraftPaths()

    def __str__(self) -> str:
        s = ""
        s += f"{self.paths}"
        return s

    def __repr__(self) -> str:
        return str(self)


CONVO_CRAFT_CONFIG = ConvoCraftConfig()
CONVO_CRAFT_PATHS = CONVO_CRAFT_CONFIG.paths

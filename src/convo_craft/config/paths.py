"""Paths and folders for data files."""

from pathlib import Path

from loguru import logger as lg

import convo_craft


class ConvoCraftPaths:
    """Paths and folders for data and resources."""

    def __init__(
        self,
    ) -> None:
        """Load the config for data folders."""
        self.load_config()

    def load_config(self) -> None:
        """Load the config for data folders."""
        self.src_fol = Path(convo_craft.__file__).parent
        self.root_fol = self.src_fol.parents[1]
        self.static_fol = self.root_fol / "static"
        self.data_fol = self.root_fol / "data"
        self.chroma_persist_fol = self.root_fol / "chroma_persist"

    def __str__(self) -> str:
        s = ""
        s += f"   ConvoCraftPaths:\n"
        s += f"           src_fol: {self.src_fol}\n"
        s += f"          root_fol: {self.root_fol}\n"
        s += f"        static_fol: {self.static_fol}\n"
        s += f"          data_fol: {self.data_fol}\n"
        s += f"chroma_persist_fol: {self.chroma_persist_fol}\n"
        return s

"""Test the convo_craft paths."""

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from convo_craft.config.paths import ConvoCraftPaths


@pytest.fixture
def convo_craft_paths() -> "ConvoCraftPaths":
    from convo_craft.config.convo_craft_config import CONVO_CRAFT_PATHS

    return CONVO_CRAFT_PATHS


def test_convo_craft_paths(convo_craft_paths: "ConvoCraftPaths") -> None:
    """Test the convo_craft paths."""
    assert convo_craft_paths.src_fol.name == "convo_craft"
    assert convo_craft_paths.root_fol.name == "convo_craft"
    assert convo_craft_paths.data_fol.name == "data"
    assert convo_craft_paths.static_fol.name == "static"
    assert convo_craft_paths.chroma_persist_fol.name == "chroma_persist"

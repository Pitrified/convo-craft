"""Test that the environment is set up correctly for VSCode."""

import os

import pytest


def test_vscode_env() -> None:
    """The environment var SAMPLE_ENV_VSCODE is available."""
    assert "SAMPLE_ENV_VSCODE" in os.environ
    assert os.environ["SAMPLE_ENV_VSCODE"] == "sample"

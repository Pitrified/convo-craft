"""Utils for the pathlib module."""

from pathlib import Path


def check_create_fol(fol: Path) -> None:
    """Check if a folder exists and create it if it doesn't.

    Args:
        fol (Path): The folder to check.
    """
    if not fol.exists():
        fol.mkdir(parents=True, exist_ok=True)

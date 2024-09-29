"""Streamlit experiments for a button bank."""

from functools import partial
from itertools import cycle

from loguru import logger as lg
import streamlit as st

from convo_craft.text.split_sentence import SentenceSplitter

ss = st.session_state


def setup_app() -> None:
    """Set up the app."""
    st.set_page_config(page_title="Button Bank", page_icon="🔘")
    st.title("Button Bank")

    init_state()


def init_state() -> None:
    """Initialize the app state."""
    if "split" not in ss:
        lg.info("Initializing app state")
        ss.split = SentenceSplitter()
        ss.words = ss.split.invoke(
            "This is a sentence."
            " A fairly long sentence."
            " Followed by another sentence."
        )
    lg.info("App state initialized")


def setup_bank() -> None:
    """Set up the button bank."""
    cols = cycle(st.columns(4))
    for i, word in enumerate(ss.words):
        col = next(cols)
        part = partial(button_with_index, word, i)
        col.button(
            f"{i}: {word}",
            key=f"button_{i}",
            on_click=part,
        )


def button_with_index(word: str, i: int) -> None:
    """Create a button with an index."""
    lg.debug(f"{i}: {word}")


def app() -> None:
    """Run the app."""
    setup_app()

    setup_bank()


if __name__ == "__main__":
    app()

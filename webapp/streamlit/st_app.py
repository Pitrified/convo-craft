"""Streamlit app for the conversation crafting project."""

from functools import partial
from itertools import cycle
import os

from loguru import logger as lg
import streamlit as st

from convo_craft.app.app import App

ss = st.session_state


def setup_app() -> None:
    """Set up the app."""
    st.set_page_config(page_title="Convo Craft", page_icon="🗣️")
    st.sidebar.title("Convo Craft")

    init_app_state()

    load_api_key()


def init_app_state() -> None:
    """Initialize the app state."""
    if "app" not in ss:
        lg.info("Initializing app state")
        ss.app = App()
    lg.info("App state initialized")


def load_api_key() -> None:
    """Load the API key."""
    st.sidebar.text_input(
        "OpenAI API key",
        key="api_key",
        type="password",
        on_change=load_api_key_cb,
    )
    a = get_app()
    if a.openai_api_key_is_set is False:
        st.write("Please enter the API key (open the sidebar)")
        st.stop()


def load_api_key_cb() -> None:
    """Load the API key callback."""
    lg.info("Loading the API key")
    a = get_app()
    a.set_openai_api_key(ss.api_key)


def get_app() -> App:
    """Get the app."""
    return ss.app


def setup_language() -> None:
    """Set up the language."""
    a: App = ss.app
    st.sidebar.subheader("Language")
    lang = a.language
    st.sidebar.write(lang.language)


def setup_topics() -> None:
    """Set up the topics."""
    st.subheader("Pick a topic")
    choose_topic()


def choose_topic() -> None:
    """Choose a topic."""
    a: App = ss.app
    at = a.topic
    # lg.debug(f'current topic index: "{at.topic_index}"')
    st.selectbox(
        "Choose a topic",
        at.topics,
        key="topic",
        index=at.topic_index,
        on_change=choose_topic_cb,
    )
    if at.topic_index is None:
        st.write("Please choose a topic")
        st.stop()
    # st.write(f'Chosen topic: "{at.topic}"')


def choose_topic_cb() -> None:
    """Choose a topic callback."""
    topic = ss.topic
    lg.info(f"Choosing topic {topic}")
    a: App = ss.app
    a.set_topic_by_value(topic)


def setup_conversation() -> None:
    """Set up the conversation."""
    # st.write(a.conversation)
    show_done_conv()
    show_current_turn()
    show_options()
    show_next_turn()


def show_done_conv() -> None:
    """Show the done conversation."""
    a: App = ss.app
    ac = a.conversation
    st.subheader("Conversation")
    # TODO should be a getter : get_done_conversation_content
    for it, turn in enumerate(ac.conversation):
        if it >= ac.conversation_step:
            break
        st.write(turn.content)


def show_current_turn() -> None:
    """Show the current turn."""
    a: App = ss.app
    ac = a.conversation
    st.write("##### Translate the next sentence:")
    st.write(ac.current_step_translation.target_text)
    st.write(ac.words.sent_guessed)
    # st.write(ac.conversation[ac.conversation_step].content)


def show_options() -> None:
    """Show the options to choose from."""
    options_dict = {
        "inactive": {
            # gray
            "type": "primary",
            "disabled": True,
        },
        "correct": {
            # gray
            "type": "secondary",
            "disabled": True,
        },
        "normal": {
            # normal
            "type": "secondary",
            "disabled": False,
        },
        "wrong": {
            # red
            "type": "primary",
            "disabled": False,
        },
    }
    # for key in options_dict: st.button(key, **options_dict[key])
    # st.subheader("Options")
    a: App = ss.app
    w = a.conversation.words
    for si, sentence in enumerate(w.words_shuffled):
        # only show the current sentence
        if si != w.current_sent:
            continue
        cols = cycle(st.columns(6))
        for wi, word in enumerate(sentence):
            col = next(cols)
            col.button(
                word.word,
                on_click=option_index_cb,
                **options_dict[word.state],
                key=f"button_options_{si}_{wi}",
                args=(si, wi),
            )
        st.divider()


def option_index_cb(sentence: int, word: int) -> None:
    """Option index callback."""
    lg.debug(f"Option index: {sentence}, {word}")
    a = get_app()
    a.receive_guess(sentence, word)


def show_next_turn() -> None:
    """Show the next turn."""
    st.button("Next Turn", on_click=show_next_turn_cb)


def show_next_turn_cb() -> None:
    """Show the next turn callback."""
    a: App = ss.app
    ac = a.conversation
    # FIXME leave the option for the user to skip the current turn
    # ! but check that we are using the correct logic
    ac.next_conversation_step()


def app() -> None:
    """Run the app."""
    setup_app()

    setup_language()

    setup_topics()

    setup_conversation()


if __name__ == "__main__":
    app()

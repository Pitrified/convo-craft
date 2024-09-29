"""Streamlit app for the conversation crafting project."""

from loguru import logger as lg
import streamlit as st

from convo_craft.app.app import App

ss = st.session_state


def setup_app() -> None:
    """Set up the app."""
    st.set_page_config(page_title="Convo Craft", page_icon="🗣️")
    st.sidebar.title("Convo Craft")

    init_state()


def init_state() -> None:
    """Initialize the app state."""
    if "app" not in ss:
        lg.info("Initializing app state")
        ss.app = App()
    lg.info("App state initialized")


def setup_language() -> None:
    """Set up the language."""
    a = ss.app
    st.sidebar.subheader("Language")
    lang = a.language
    st.sidebar.write(lang)


def setup_topics() -> None:
    """Set up the topics."""
    a = ss.app
    st.sidebar.subheader("Topics")
    topics = a.topics
    if len(topics) == 0:
        a.generate_topics()
    choose_topic()


def choose_topic() -> None:
    """Choose a topic."""
    a = ss.app
    lg.debug(f'current topic index: "{a.topic_index}"')
    st.sidebar.selectbox(
        "Choose a topic",
        a.topics,
        key="topic",
        index=a.topic_index,
        on_change=choose_topic_cb,
    )
    if a.topic_index is None:
        st.write("Please choose a topic")
        st.stop()
    st.write(f'Chosen topic: "{a.topic}"')


def choose_topic_cb() -> None:
    """Choose a topic callback."""
    topic = ss.topic
    lg.info(f"Choosing topic {topic}")
    a = ss.app
    a.set_topic(topic)


def setup_conversation() -> None:
    """Set up the conversation."""
    a = ss.app
    if len(a.conversation) == 0:
        a.generate_conversation()
    # st.write(a.conversation)
    show_done_conv()
    show_current_turn()
    show_next_turn()


def show_done_conv() -> None:
    """Show the done conversation."""
    a = ss.app
    st.subheader("Conversation")
    for it, turn in enumerate(a.conversation):
        if it >= a.conversation_step:
            break
        st.write(turn.content)


def show_current_turn() -> None:
    """Show the current turn."""
    a = ss.app
    st.subheader("Current Turn")
    st.write(a.conversation[a.conversation_step].content)
    st.write(a.current_step_translation)


def show_next_turn() -> None:
    """Show the next turn."""
    st.button(
        "Next Turn",
        on_click=show_next_turn_cb,
    )


def show_next_turn_cb() -> None:
    """Show the next turn callback."""
    a: App = ss.app
    a.next_conversation_step()


def app() -> None:
    """Run the app."""
    setup_app()

    setup_language()

    setup_topics()

    setup_conversation()


if __name__ == "__main__":
    app()

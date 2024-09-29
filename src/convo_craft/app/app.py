"""An app for the Convo Craft project."""

from loguru import logger as lg

from convo_craft.llm.conversation_generator import (
    CONVERSATION_SAMPLE,
    TOPIC_SAMPLE,
    ConversationGenerator,
    ConversationTurn,
)
from convo_craft.llm.topic_picker import OLD_TOPICS, TopicsPicker
from convo_craft.llm.translator import Translator

LANGUAGE_OPTIONS = ["Brazilian Portuguese"]


class App:
    """An app for the Convo Craft project."""

    def __init__(self) -> None:
        """Initialize the app."""
        self.reset_state()

    def reset_state(self) -> None:
        """Reset the app state."""
        self.language_options = LANGUAGE_OPTIONS
        self.set_language_index(0)

        self.set_topics([])

        # MAYBE simplify this by not calling it now
        #     ? and just initializing it when the actual conversation starts
        self.set_conversation([])

    def set_language_index(self, language_index: int) -> None:
        """Set the language index."""
        self.language_index = language_index
        self.language = self.language_options[self.language_index]

    def set_topics(self, topics: list[str]) -> None:
        """Set the topics."""
        self.topics = topics
        self.set_topic_index(None)
        if len(self.topics) == 0:
            self.topic = ""

    def set_topic(self, topic: str) -> None:
        """Set the topic."""
        # find the index of the topic
        new_topic_index = self.topics.index(topic)
        lg.debug(f"Setting topic: {topic} at index: {new_topic_index}")
        self.set_topic_index(new_topic_index)

    def set_topic_index(self, topic_index: int | None) -> None:
        """Set the topic index."""
        self.topic_index = topic_index
        if self.topic_index is not None:
            self.topic = self.topics[self.topic_index]
        # reset the conversation state
        self.set_conversation([])

    def generate_topics(self) -> None:
        """Generate topics."""
        lg.info("Generating topics")
        tp = TopicsPicker(
            language=self.language,
            understanding_level="intermediate",
        )
        res = tp.invoke(OLD_TOPICS)
        self.set_topics(res.topics)

    def set_conversation(self, conversation: list[ConversationTurn]) -> None:
        """Set the conversation."""
        self.conversation = conversation
        if len(self.conversation) == 0:
            self.set_conversation_step(None)
        else:
            self.set_conversation_step(0)

    def set_conversation_step(self, conversation_step: int | None) -> None:
        """Set the conversation step."""
        lg.info(f"Setting conversation step: {conversation_step}")
        self.conversation_step = conversation_step
        if self.conversation_step is not None:
            self.current_step_translation = self.translate(
                self.conversation[self.conversation_step].content
            )

    def next_conversation_step(self) -> None:
        """Go to the next conversation step."""
        if self.conversation_step is None:
            self.set_conversation_step(0)
        else:
            self.set_conversation_step(self.conversation_step + 1)

    def translate(self, text: str) -> str:
        """Translate the text."""
        lg.debug(f"Translating: {text}")
        t = Translator(
            source_language=self.language,
            target_language="English",
        )
        res = t.invoke(text)
        return res.target_text

    def generate_conversation(self) -> None:
        """Generate a conversation."""
        lg.info("Generating conversation")
        c = ConversationGenerator(
            language=self.language,
            num_messages=5,
            num_sentences=3,
            understanding_level="intermediate",
            conversation_sample=CONVERSATION_SAMPLE,
            topic_sample=TOPIC_SAMPLE,
        )
        conv = c.invoke(self.topic)
        lg.debug(f"{conv=}")
        self.set_conversation(conv.turns)

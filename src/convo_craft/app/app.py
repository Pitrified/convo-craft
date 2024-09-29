"""An app for the Convo Craft project."""

from dataclasses import dataclass
import random

from loguru import logger as lg

from convo_craft.llm.conversation_generator import (
    CONVERSATION_SAMPLE,
    TOPIC_SAMPLE,
    ConversationGenerator,
    ConversationTurn,
)
from convo_craft.llm.paragraph_splitter import ParagraphSplitter
from convo_craft.llm.topic_picker import OLD_TOPICS, TopicsPicker
from convo_craft.llm.translator import Translator
from convo_craft.text.split_sentence import SentenceSplitter

LANGUAGE_OPTIONS = ["Brazilian Portuguese"]


class AppLanguage:
    """Language picker for the app."""

    def __init__(self) -> None:
        self.language_options = LANGUAGE_OPTIONS
        self.set_language_index(0)

    def set_language_index(self, language_index: int) -> None:
        """Set the language index."""
        self.language_index = language_index
        self.language = self.language_options[self.language_index]


class AppTopic:
    """Topic picker for the app."""

    def __init__(self) -> None:
        # setup tools
        self.tp = TopicsPicker(understanding_level="intermediate")
        # init the topic
        self.topic = ""
        self.topic_index = None
        # generate the topics
        self.generate_topics()

    def generate_topics(self) -> None:
        """Generate topics."""
        lg.info("Generating topics")
        tp = TopicsPicker(
            understanding_level="intermediate",
        )
        res = tp.invoke(OLD_TOPICS)
        self.set_topics(res.topics)

    def set_topics(self, topics: list[str]) -> None:
        """Set the topics."""
        self.topics = topics
        self.set_topic_by_index(None)

    def set_topic_by_value(self, topic: str) -> None:
        """Set the topic."""
        # find the index of the topic
        new_topic_index = self.topics.index(topic)
        lg.debug(f"Setting topic: {topic} at index: {new_topic_index}")
        self.set_topic_by_index(new_topic_index)

    def set_topic_by_index(self, topic_index: int | None) -> None:
        """Set the topic index."""
        self.topic_index = topic_index
        if self.topic_index is not None:
            self.topic = self.topics[self.topic_index]
        # NOTE reset the conversation state


class AppConversation:
    """Conversation picker for the app."""

    def __init__(
        self,
        topic: str,
        language: AppLanguage,
    ) -> None:
        """Initialize the conversation picker."""
        # setup configuration
        self.topic = topic
        self.language = language
        # setup tools
        self.setup_tools()
        # generate the conversation
        self.generate_conversation()

    def setup_tools(self) -> None:
        self.cg = ConversationGenerator(
            language=self.language.language,
            num_messages=5,
            num_sentences=3,
            understanding_level="intermediate",
            conversation_sample=CONVERSATION_SAMPLE,
            topic_sample=TOPIC_SAMPLE,
        )
        self.translator = Translator(
            source_language=self.language.language,
            target_language="English",
        )

    def generate_conversation(self) -> None:
        """Generate a conversation."""
        lg.info("Generating conversation")
        conv = self.cg.invoke(self.topic)
        lg.debug(f"{conv=}")
        self.conversation: list[ConversationTurn] = conv.turns
        self.set_conversation_step(0)

    def set_conversation_step(self, conversation_step: int) -> None:
        """Set the conversation step."""
        lg.info(f"Setting conversation step: {conversation_step}")
        self.conversation_step = conversation_step
        current_step = self.conversation[self.conversation_step].content
        self.current_step_translation = self.translator.invoke(current_step)
        self.words = AppWords(current_step)

    def next_conversation_step(self) -> None:
        """Go to the next conversation step."""
        self.set_conversation_step(self.conversation_step + 1)


@dataclass
class AppWordGuess:
    word: str
    state: str


class AppWords:
    """The words related to the current step in the conversation."""

    def __init__(self, current_step: str) -> None:
        """Initialize the app words."""
        # setup tools
        self.para_splitter = ParagraphSplitter()
        self.sent_splitter = SentenceSplitter()
        # split the paragraph into sentences and words
        self.paragraph = current_step
        self.para_split_result = self.para_splitter.invoke(self.paragraph)
        self.sentences = self.para_split_result.portions
        self.sents_words: list[list[AppWordGuess]] = []
        for sent in self.sentences:
            words = self.sent_splitter.invoke(sent)
            w_guess = [AppWordGuess(word=word, state="normal") for word in words]
            self.sents_words.append(w_guess)
        # init the user guess
        self.current_sent = 0
        self.current_word = 0
        # shuffle the words
        self.shuffle_words()
        # set the done flag
        self.done = False

    def shuffle_words(self) -> None:
        """Shuffle the words."""
        self.words_shuffled = []
        for sent_words in self.sents_words:
            words_shuffled = sent_words.copy()
            random.shuffle(words_shuffled)
            self.words_shuffled.append(words_shuffled)

    def receive_guess(self, guess: str) -> bool:
        """Receive a guess."""
        # grab the current word
        current_word = self.sents_words[self.current_sent][self.current_word]
        # check if the guess is wrong
        if not guess == current_word.word:
            current_word.state = "wrong"
            return False
        # mark the word as correct
        current_word.state = "correct"
        # move to the next word
        self.current_word += 1
        if self.current_word == len(self.sents_words[self.current_sent]):
            self.current_sent += 1
            self.current_word = 0
        # check if done
        if self.current_sent == len(self.sents_words):
            self.done = True
        return True


class App:
    """An app for the Convo Craft project."""

    def __init__(self) -> None:
        """Initialize the app."""
        self.reset_language()
        self.reset_topic()

    def reset_language(self) -> None:
        """Reset the language."""
        self.language = AppLanguage()

    def reset_topic(self) -> None:
        """Reset the topic."""
        self.topic = AppTopic()

    def set_topic_by_value(self, topic: str) -> None:
        """Set the topic."""
        self.topic.set_topic_by_value(topic)
        self.conversation = AppConversation(
            topic=self.topic.topic,
            language=self.language,
        )

"""An app for the Convo Craft project."""

from dataclasses import dataclass
import random

from loguru import logger as lg

from convo_craft.config.chat_openai import ChatOpenAIConfig
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
from convo_craft.utils.u_pydantic import convert_to_secret_str_v2

LANGUAGE_OPTIONS = ["Brazilian Portuguese"]


class AppLanguage:
    """Language picker for the app."""

    def __init__(
        self,
        app: "App",
    ) -> None:
        # save reference to the app
        self.app = app
        # setup the language options
        self.language_options = LANGUAGE_OPTIONS
        self.set_language_index(0)

    def set_language_index(self, language_index: int) -> None:
        """Set the language index."""
        self.language_index = language_index
        self.language = self.language_options[self.language_index]


class AppTopic:
    """Topic picker for the app."""

    def __init__(
        self,
        app: "App",
        understanding_level="intermediate",
    ) -> None:
        # save reference to the app
        self.app = app
        # setup tools
        self.tp = TopicsPicker(
            chat_openai_config=self.app.struct_llm_config,
            understanding_level=understanding_level,
        )
        # init the topic
        self.topic = ""
        self.topic_index = None
        # generate the topics
        self.generate_topics()

    def generate_topics(self) -> None:
        """Generate topics."""
        lg.info("Generating topics")
        res = self.tp.invoke(OLD_TOPICS)
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
        app: "App",
    ) -> None:
        """Initialize the conversation picker."""
        # save reference to the app
        self.app = app
        # setup configuration
        self.topic = self.app.topic.topic
        self.language = self.app.language
        # setup tools
        self.setup_tools()
        # generate the conversation
        self.generate_conversation()
        # init the conversation state
        self.done = False

    def setup_tools(self) -> None:
        self.cg = ConversationGenerator(
            chat_openai_config=self.app.struct_llm_config,
            language=self.language.language,
            num_messages=5,
            num_sentences=3,
            understanding_level="intermediate",
            conversation_sample=CONVERSATION_SAMPLE,
            topic_sample=TOPIC_SAMPLE,
        )
        self.translator = Translator(
            chat_openai_config=self.app.struct_llm_config,
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
        self.words = AppWords(app=self.app, current_step=current_step)

    def next_conversation_step(self) -> None:
        """Go to the next conversation step."""
        if self.conversation_step == len(self.conversation) - 1:
            lg.info("Conversation is done")
            self.done = True
            return
        self.set_conversation_step(self.conversation_step + 1)

    def receive_guess(self, shuf_si: int, shuf_wi: int) -> None:
        """Receive a guess."""
        self.words.receive_guess(shuf_si, shuf_wi)
        if self.words.done:
            self.next_conversation_step()


@dataclass
class AppWordGuess:
    word: str
    state: str


class AppWords:
    """The words related to the current step in the conversation."""

    def __init__(
        self,
        app: "App",
        current_step: str,
    ) -> None:
        """Initialize the app words."""
        # save reference to the app
        self.app = app
        # setup tools
        self.para_splitter = ParagraphSplitter(
            chat_openai_config=self.app.struct_llm_config,
        )
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
        # accumulate the correct words as they are guessed
        self.sent_guessed = ""

    def shuffle_words(self) -> None:
        """Shuffle the words."""
        self.words_shuffled: list[list[AppWordGuess]] = []
        for sent_words in self.sents_words:
            words_shuffled = sent_words.copy()
            random.shuffle(words_shuffled)
            self.words_shuffled.append(words_shuffled)

    def receive_guess(self, shuf_si: int, shuf_wi: int) -> bool:
        """Receive a guess."""
        # grab the guessed word from the shuffled list
        guess = self.words_shuffled[shuf_si][shuf_wi]
        lg.debug(f"Received guess: {guess} at {shuf_si}, {shuf_wi}")
        # grab the current word
        current_word = self.sents_words[self.current_sent][self.current_word]
        # check if the guess is wrong
        if not guess.word == current_word.word:
            guess.state = "wrong"
            lg.debug(f"Wrong guess: {guess} != {current_word}")
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
            lg.success("All words guessed correctly")
            self.done = True
        # add the word to the guessed sentence
        self.sent_guessed += f"{guess.word} "
        lg.debug(f"Right guess: {guess} == {current_word}")
        return True


class App:
    """An app for the Convo Craft project."""

    def __init__(self) -> None:
        """Initialize the app."""
        self.reset_openai_api_key()
        self.reset_language()

    def reset_openai_api_key(self) -> None:
        """Reset the OpenAI API key."""
        self.openai_api_key = convert_to_secret_str_v2("not set")
        self.openai_api_key_is_set = False

    def set_openai_api_key(self, openai_api_key: str) -> None:
        """Set the OpenAI API key."""
        self.openai_api_key = convert_to_secret_str_v2(openai_api_key)
        self.openai_api_key_is_set = True
        self.set_llm_config()
        self.reset_topic()

    def set_llm_config(self) -> None:
        """Set the LLM config."""
        self.struct_llm_config = ChatOpenAIConfig(api_key=self.openai_api_key)

    def reset_language(self) -> None:
        """Reset the language."""
        self.language = AppLanguage(self)

    def reset_topic(self) -> None:
        """Reset the topic."""
        self.topic = AppTopic(self)

    def set_topic_by_value(self, topic: str) -> None:
        """Set the topic."""
        self.topic.set_topic_by_value(topic)
        self.conversation = AppConversation(app=self)

    def receive_guess(self, shuf_si: int, shuf_wi: int) -> None:
        """Receive a guess."""
        self.conversation.receive_guess(shuf_si, shuf_wi)
        if self.conversation.done:
            lg.success("Conversation is done")

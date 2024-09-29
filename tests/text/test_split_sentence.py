"""Test the sentence splitting module."""

import pytest

from convo_craft.text.split_sentence import SentenceSplitter


@pytest.fixture
def sentence_splitter_default() -> SentenceSplitter:
    """Return a sentence splitter with default settings."""
    return SentenceSplitter()


def test_sentence_splitter(sentence_splitter_default: SentenceSplitter) -> None:
    """Test the sentence splitter."""
    sentence = "This is a sentence."
    words = sentence_splitter_default.invoke(sentence)
    assert words == ["This", "is a", "sentence."]


def test_empty_sentence(sentence_splitter_default: SentenceSplitter) -> None:
    """Test an empty sentence."""
    sentence = ""
    words = sentence_splitter_default.invoke(sentence)
    assert words == []


@pytest.fixture
def sentence_splitter_long_words() -> SentenceSplitter:
    """Return a sentence splitter with long word settings."""
    return SentenceSplitter(min_word_len=5)


def test_long_words(sentence_splitter_long_words: SentenceSplitter) -> None:
    """Test long words."""
    sentence = "This is a sentence."
    words = sentence_splitter_long_words.invoke(sentence)
    assert words == ["This is", "a sentence."]

"""Split a sentence down to words."""

from dataclasses import dataclass


@dataclass
class SentenceSplitter:
    """A sentence splitter."""

    min_word_len: int = 3

    def invoke(self, sentence: str) -> list[str]:
        """Split the sentence.

        If a word is too short, combine it with the next word.
        TODO might want to use a more sophisticated algorithm,
             merging more than two words if necessary.
             No need to overcomplicate it for now.
        """
        words = sentence.split()
        # if a word is too short, combine it with the next word
        combined_words = []
        i = 0
        while i < len(words):
            word = words[i]
            if len(word) < self.min_word_len and i < len(words) - 1:
                next_word = words[i + 1]
                combined_word = f"{word} {next_word}"
                combined_words.append(combined_word)
                i += 2
            else:
                combined_words.append(word)
                i += 1
        return combined_words

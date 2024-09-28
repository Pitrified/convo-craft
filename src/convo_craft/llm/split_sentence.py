"""Sentence splitter module."""

from dataclasses import dataclass

from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class SplitSentenceResult(BaseModel):
    """The result of splitting a sentence.

    The original sentence should be split into portions without changing the text,
    such that the concatenation of the portions should be equal to the original sentence.

    Prefer splitting the sentence into meaningful portions, such as phrases or clauses.
    """

    portions: list[str] = Field(description="The split sentence.")


split_sentence_template = """Split the following sentence into portions:

{sentence}
"""
split_sentence_prompt = ChatPromptTemplate(
    [HumanMessagePromptTemplate.from_template(split_sentence_template)]
)


@dataclass
class SentenceSplitter:
    """A sentence splitter."""

    def __post_init__(self):
        """Initialize the sentence splitter."""
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.structured_llm = self.model.with_structured_output(SplitSentenceResult)

    def invoke(self, sentence: str) -> SplitSentenceResult:
        """Split the sentence."""
        split_sentence_value = split_sentence_prompt.invoke({"sentence": sentence})
        output = self.structured_llm.invoke(split_sentence_value)
        if not isinstance(output, SplitSentenceResult):
            raise ValueError(f"Unexpected output type: {type(output)}")
        return output

"""Paragraph splitter module."""

from dataclasses import dataclass

from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from convo_craft.config.chat_openai import ChatOpenAIConfig


class ParagraphSplitterResult(BaseModel):
    """The result of splitting a paragraph.

    The original paragraph should be split into portions without changing the text,
    such that the concatenation of the portions should be equal to the original paragraph.

    Prefer splitting the paragraph into meaningful portions, such as phrases or clauses.
    Avoid splitting on commas, unless the sentence is longer than 15 words.
    Avoid generating a single word as a portion.
    """

    portions: list[str] = Field(description="The split paragraph.")


split_paragraph_template = """Split the following paragraph into portions:

{paragraph}
"""
split_paragraph_prompt = ChatPromptTemplate(
    [HumanMessagePromptTemplate.from_template(split_paragraph_template)]
)


@dataclass
class ParagraphSplitter:
    """A paragraph splitter."""

    chat_openai_config: ChatOpenAIConfig

    def __post_init__(self):
        """Initialize the paragraph splitter."""
        self.model = ChatOpenAI(**self.chat_openai_config.model_dump())
        self.structured_llm = self.model.with_structured_output(ParagraphSplitterResult)

    def invoke(self, paragraph: str) -> ParagraphSplitterResult:
        """Split the paragraph."""
        split_paragraph_value = split_paragraph_prompt.invoke({"paragraph": paragraph})
        output = self.structured_llm.invoke(split_paragraph_value)
        if not isinstance(output, ParagraphSplitterResult):
            raise ValueError(f"Unexpected output type: {type(output)}")
        return output

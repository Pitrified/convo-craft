"""Translator module."""

from dataclasses import dataclass

from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class TranslatorResult(BaseModel):
    """The result of a translation."""

    target_text: str = Field(description="The translated text")


translation_template = """Translate the following text from {source_language} to {target_language}:

{source_text}
"""
translation_prompt = ChatPromptTemplate(
    [HumanMessagePromptTemplate.from_template(translation_template)]
)


@dataclass
class Translator:
    """A translator."""

    source_language: str
    target_language: str

    def __post_init__(self):
        """Initialize the translator."""
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.structured_llm = self.model.with_structured_output(TranslatorResult)

    def invoke(self, source_text: str) -> TranslatorResult:
        """Translate the text."""
        translation_value = translation_prompt.invoke(
            {
                "source_language": self.source_language,
                "target_language": self.target_language,
                "source_text": source_text,
            }
        )
        output = self.structured_llm.invoke(translation_value)
        if not isinstance(output, TranslatorResult):
            raise ValueError(f"Unexpected output type: {type(output)}")
        return output

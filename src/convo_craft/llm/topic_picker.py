"""Topic picker module."""

from dataclasses import dataclass
from enum import Enum

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from convo_craft.config.chat_openai import ChatOpenAIConfig


class TopicsPickerResult(BaseModel):
    """Options for new topics for a conversation.

    Each topic should be a sentence describing the topic.
    """

    topics: list[str] = Field(description="The list of topics")


topic_picker_template = """Generate a list of topics for a conversation \
that should be used to teach the user the language.
Assume that the user has an {understanding_level} level of understanding of the language.

Here are some options already in the system, generate new topics for the user:
{old_topics}
"""
topic_picker_prompt = ChatPromptTemplate(
    [SystemMessagePromptTemplate.from_template(topic_picker_template)]
)

OLD_TOPICS = [
    "How to order food at a restaurant",
    "How to ask for directions",
    "Traveling to a foreign country",
    "Talking about the weather",
    "Introducing yourself",
    "Talking about your family",
    "Going to the doctor",
    "Talking about your hobbies",
]


@dataclass
class TopicsPicker:
    """A topic picker."""

    chat_openai_config: ChatOpenAIConfig
    understanding_level: str

    def __post_init__(self):
        """Initialize the topic picker."""
        self.model = ChatOpenAI(**self.chat_openai_config.model_dump())
        self.structured_llm = self.model.with_structured_output(TopicsPickerResult)

    def invoke(self, old_topics: list[str]) -> TopicsPickerResult:
        """Pick a topic."""
        old_topics_str = "\n".join(old_topics)
        topic_picker_value = topic_picker_prompt.invoke(
            {
                "understanding_level": self.understanding_level,
                "old_topics": old_topics_str,
            }
        )
        output = self.structured_llm.invoke(topic_picker_value)
        if not isinstance(output, TopicsPickerResult):
            raise ValueError(f"Unexpected output type: {type(output)}")
        return output

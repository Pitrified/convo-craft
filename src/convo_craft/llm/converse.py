"""Conversation crafting module."""

from dataclasses import dataclass
from enum import Enum

from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class ConversationRole(Enum):
    """The role of the speaker."""

    USER = "user"
    SYSTEM = "system"


class ConversationTurn(BaseModel):
    """A conversation turn."""

    role: ConversationRole = Field(description="The role of the speaker")
    content: str = Field(description="The content of the message")


class Conversation(BaseModel):
    """A conversation with a consistent plot or theme.

    The roles in the turns should alternate between two speakers, identified as
    the user and the system.
    """

    turns: list[ConversationTurn] = Field(description="The turns of the conversation")


conversation_template = """Write a conversation in {language} between two persons, \
that should be used to teach the user the language.
The conversation should be about the following topic: "{topic}".
Assume that the user has an intermediate level of understanding of the language.
The conversation should last about {num_msg} messages in total, with each message being about 2-3 sentences long.
"""
conversation_prompt = ChatPromptTemplate(
    [HumanMessagePromptTemplate.from_template(conversation_template)]
)


@dataclass
class ConversationGenerator:
    """Generate a conversation."""

    language: str
    num_msg: int

    def __post_init__(self) -> None:
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.structured_llm = self.model.with_structured_output(Conversation)

    def generate(self, topic: str) -> Conversation:
        """Generate a conversation."""
        conversation_value = conversation_prompt.invoke(
            {
                "language": self.language,
                "topic": topic,
                "num_msg": self.num_msg,
            }
        )
        output = self.structured_llm.invoke(conversation_value)
        if not isinstance(output, Conversation):
            raise ValueError(f"Invalid output: {output}")
        return output

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


class ConversationGeneratorResult(BaseModel):
    """A conversation with a consistent plot or theme.

    The roles in the turns should alternate between two speakers, identified as
    the user and the system.
    """

    turns: list[ConversationTurn] = Field(description="The turns of the conversation")


conversation_template = """Write a conversation in {language} between two persons, \
that should be used to teach the user the language.
The conversation should be about the following topic: "{topic}".
Assume that the user has an {understanding_level} level of understanding of the language.
The conversation should last about {num_msg} messages in total, with each message being about 2-3 sentences long.
"""
difficulty_template = """This is an example of a conversation in {language} between two persons, \
of the appropriate difficulty level for the user, which is {understanding_level}:
{conversation_sample}
"""
conversation_prompt = ChatPromptTemplate(
    [
        HumanMessagePromptTemplate.from_template(conversation_template),
        HumanMessagePromptTemplate.from_template(difficulty_template),
    ],
)

CONVERSATION_SAMPLE = """Oi! Você já decidiu o que vai pedir no restaurante?
Oi! Eu estou pensando em pedir uma pizza. E você, o que vai escolher?
Eu estou em dúvida entre o hambúrguer e a salada. Você já experimentou o hambúrguer daqui?
Sim, eu já experimentei! O hambúrguer é muito saboroso e vem com batatas fritas. Você gosta de batatas fritas?
Gosto sim! E a pizza, qual sabor você recomenda?
Eu recomendo a pizza de margherita. É simples, mas deliciosa! Você prefere pizza com ou sem borda recheada?
Prefiro com borda recheada! E você, vai pedir alguma bebida?
Sim, eu vou pedir uma limonada. E você, vai querer algo para beber também?
Acho que vou pedir uma cerveja. Você sabe se eles têm opções artesanais?
Sim, eles têm algumas opções de cervejas artesanais. Vou perguntar ao garçom quando ele vier.
Ótima ideia! Vamos fazer o pedido assim que o garçom chegar.
"""


@dataclass
class ConversationGenerator:
    """Generate a conversation."""

    language: str
    num_msg: int
    understanding_level: str
    conversation_sample: str

    def __post_init__(self) -> None:
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.structured_llm = self.model.with_structured_output(
            ConversationGeneratorResult
        )

    def invoke(self, topic: str) -> ConversationGeneratorResult:
        """Generate a conversation."""
        conversation_value = conversation_prompt.invoke(
            {
                "language": self.language,
                "topic": topic,
                "understanding_level": self.understanding_level,
                "num_msg": self.num_msg,
                "conversation_sample": self.conversation_sample,
            }
        )
        output = self.structured_llm.invoke(conversation_value)
        if not isinstance(output, ConversationGeneratorResult):
            raise ValueError(f"Invalid output: {output}")
        return output

from openai import OpenAI
from pydantic import BaseModel, Field


class Step(BaseModel):
    explanation: str = Field(description="Explanation of the step")
    output: str = Field(description="Output of the step")


class MathResponse(BaseModel):
    steps: list[Step] = Field(description="List of steps to solve the math problem")
    final_answer: str = Field(description="Final answer of the math problem")


client = OpenAI()

completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor."},
        {"role": "user", "content": "solve 8x + 31 = 2"},
    ],
    response_format=MathResponse,
)

message = completion.choices[0].message
if message.parsed:
    print(message.parsed.steps)
    print(message.parsed.final_answer)
else:
    print(message.refusal)

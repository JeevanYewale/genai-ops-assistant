from openai import OpenAI
from pydantic import BaseModel
from typing import Any
import os
from dotenv import load_dotenv

load_dotenv()


class PlanSchema(BaseModel):
    steps: list[str]
    tools_needed: list[str]


class FinalOutput(BaseModel):
    result: str
    sources: list[str]


client = OpenAI(api_key=os.getenv("LLM_API_KEY"))


def call_llm(prompt: str, schema: type[BaseModel]) -> Any:
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "response",
                "schema": schema.model_json_schema(),
            },
        },
    )
    return schema.model_validate_json(response.choices[0].message.content).model_dump()

import json
import logging
import uuid
from typing import Literal, TypedDict, TypeVar

import aiohttp
from dotenv import load_dotenv

from language_evaluator.backend.generic import LLMInterface, PromptReply
from language_evaluator.prompt import Prompt

try:
    load_dotenv()
    # Attempt load - but it's non-critical
except BaseException:
    pass

import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential

from language_evaluator.config.openai import OpenAIConfig

T = TypeVar("T")

logger = logging.getLogger(__name__)


class OpenAIInputMessage(TypedDict):
    role: str
    content: str


class MessageResponse(TypedDict):
    role: str
    content: str


class ChoiceResponse(TypedDict):
    index: int
    message: MessageResponse


class OpenAIRawResponse(TypedDict):
    id: str
    object: str
    created: int
    model: str
    choices: list[ChoiceResponse]


async def reformat_json(text: str) -> str:
    return await chat_completion_request(
        messages=[
            {
                "role": "system",
                "content": "You reformat text into valid JSON. You do not add comments or messages.",
            },
            {"role": "user", "content": text},
        ],
        model="gpt-3.5-turbo",
    )


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
async def chat_completion_request(
    messages: list[OpenAIInputMessage],
    functions: str | None = None,
    function_call: str | None = None,
    model: str = OpenAIConfig.from_env().evaluation_model,
) -> str:
    request_uuid = uuid.uuid4()
    assert openai.api_key is not None
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        logger.info(f"[{request_uuid}] Started Chat Completion Request")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=json_data,
            ) as response:
                formatted_response: OpenAIRawResponse = await response.json()
                logger.info(f"[{request_uuid}] Finished Chat Completion Request")
                return formatted_response["choices"][-1]["message"]["content"]
    except Exception as e:
        logger.error("Unable to generate ChatCompletion response")
        logger.error(f"Exception: {e}")
        raise e


OPENAI_MODELS = Literal["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4"]


class OpenAIBackend(LLMInterface):
    def __init__(self, model: OPENAI_MODELS):
        self.model = model

    def name(self) -> str:
        return f"OpenAI-{self.model}"

    async def prompt(self, prompt: Prompt) -> PromptReply:
        formatted_prompt: list[OpenAIInputMessage] = [
            {"role": "system", "content": prompt.system_message()},
            {"role": "user", "content": prompt.user_message()},
        ]
        response = await chat_completion_request(
            messages=formatted_prompt,
            functions=None,
            function_call=None,
            model=self.model,
        )
        return PromptReply(json.dumps(formatted_prompt), response)

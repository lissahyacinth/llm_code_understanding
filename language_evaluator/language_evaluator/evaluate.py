import asyncio
from dataclasses import dataclass

from language_evaluator.backend.generic import LLMInterface
from language_evaluator.backend.openai import OpenAIBackend
from language_evaluator.backend.xwin import XWinBackend
from language_evaluator.code_sample.prompt import CodeSamplePrompt


@dataclass
class ModelAnswer:
    model_name: str
    prompt: CodeSamplePrompt
    reply: str


async def generate_all_answers(
    prompts: list[CodeSamplePrompt],
) -> list[ModelAnswer]:
    model_backend: LLMInterface
    model_answers: list[ModelAnswer] = []
    for model_backend in [
        OpenAIBackend("gpt-3.5-turbo"),
        OpenAIBackend("gpt-4"),
        XWinBackend(),
    ]:
        model_replies: list[str] = await asyncio.gather(
            *(model_backend.prompt(prompt) for prompt in prompts)
        )
        model_answers.extend(
            (
                ModelAnswer(model_backend.name(), prompt, reply)
                for (prompt, reply) in zip(prompts, model_replies)
            )
        )
    return model_answers

import asyncio
from dataclasses import dataclass

from language_evaluator.backend.generic import LLMInterface
from language_evaluator.backend.openai import OpenAIBackend
from language_evaluator.backend.xwin import XWinBackend
from language_evaluator.code_sample.prompt import CodeSamplePrompt
from language_evaluator.evaluation.parse import EvaluationReply
from language_evaluator.evaluation.prompt import EvaluationPrompt


@dataclass
class ModelAnswer:
    model_name: str
    prompt: CodeSamplePrompt
    ideal_answer: str
    reply: str


async def generate_all_answers(
        prompts: list[tuple[str, CodeSamplePrompt]],
) -> list[ModelAnswer]:
    model_backend: LLMInterface
    model_answers: list[ModelAnswer] = []
    for model_backend in [
        OpenAIBackend("gpt-3.5-turbo"),
        OpenAIBackend("gpt-4"),
        XWinBackend(),
    ]:
        model_replies: list[str] = await asyncio.gather(
            *(model_backend.prompt(prompt) for (_ideal_answer, prompt) in prompts)
        )
        model_answers.extend(
            (
                ModelAnswer(model_backend.name(), prompt, ideal_answer, reply)
                for ((ideal_answer, prompt), reply) in zip(prompts, model_replies)
            )
        )
    return model_answers


async def grade_all_answers(
        answers: list[tuple[str, ModelAnswer]]
) -> list[tuple[ModelAnswer, EvaluationReply]]:
    evaluation_backend = OpenAIBackend("gpt-4")
    replies: list[tuple[ModelAnswer, EvaluationReply]] = []
    for (model_answer, answer) in answers:
        eval_prompt = EvaluationPrompt(
            function_code=answer.prompt.user_message(),
            previous_documentation=model_answer,
            new_documentation=answer.reply
        )
        grade = await evaluation_backend.prompt(eval_prompt)
        formatted_grade = EvaluationReply.from_string_reply(grade.reply)
        replies.append((answer, formatted_grade))
    return replies

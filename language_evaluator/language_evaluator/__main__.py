import asyncio
import pathlib

import click

from language_evaluator.data import load_test_examples
from language_evaluator.evaluate import generate_all_answers, grade_all_answers, ModelAnswer
from language_evaluator.evaluation.parse import EvaluationReply


@click.command()
@click.option("--example_directory", type=str, required=True)
def evaluate(example_directory: str):
    formatted_example_directory = pathlib.Path(example_directory)
    if (
        not formatted_example_directory.exists()
        or not formatted_example_directory.is_dir()
    ):
        raise ValueError(f"Could not find a directory at {example_directory}")
    examples = list(load_test_examples(formatted_example_directory))
    answers = (
        asyncio.run(
            generate_all_answers(
                [
                    (test.ideal_answer, test.as_prompt())
                    for test in examples
                ]
            )
        )
    )
    graded_answers = asyncio.run(grade_all_answers(
        answers
    ))
    model_answer: ModelAnswer
    evaluation: EvaluationReply
    for (model_answer, evaluation) in graded_answers:
        print(f"{model_answer.model_name} replied with {model_answer.reply}")
        print(f"This answer received a grade of {evaluation.new_rating} due to {evaluation.new_grade_reasoning}")


if __name__ == "__main__":
    evaluate()

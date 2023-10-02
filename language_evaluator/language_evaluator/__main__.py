import asyncio
import pathlib

import click

from language_evaluator.data import load_test_examples
from language_evaluator.evaluate import generate_all_answers


@click.command()
@click.option("--example_directory", type=str, required=True)
def evaluate(example_directory: str):
    formatted_example_directory = pathlib.Path(example_directory)
    if (
        not formatted_example_directory.exists()
        or not formatted_example_directory.is_dir()
    ):
        raise ValueError(f"Could not find a directory at {example_directory}")
    print(
        asyncio.run(
            generate_all_answers(
                [
                    test.as_prompt()
                    for test in list(load_test_examples(formatted_example_directory))
                ]
            )
        )
    )


if __name__ == "__main__":
    evaluate()

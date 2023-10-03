import pathlib
from typing import Iterator

from language_evaluator.code_sample.sample import CodeExample


def load_test_examples(root_directory: pathlib.Path) -> Iterator[CodeExample]:
    for prompt_file in root_directory.glob("**/prompt.txt"):
        yield CodeExample.load_from_directory(prompt_file.parent)

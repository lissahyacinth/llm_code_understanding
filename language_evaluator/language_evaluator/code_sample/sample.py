from __future__ import annotations

import pathlib
from dataclasses import dataclass

from language_evaluator.code_sample.prompt import CodeSamplePrompt


@dataclass
class CodeExample:
    _code_sample: list[str]
    _prompt: str
    _result: str
    _lineno: int  # Split point for prefix/suffix

    @classmethod
    def load_from_directory(cls, directory_path: pathlib.Path) -> CodeExample:
        if not directory_path.exists() or not directory_path.is_dir():
            raise ValueError(f"{directory_path} does not exist as a directory")
        with open(directory_path / "blank.py", encoding="utf-8") as f:
            code_sample = f.readlines()
        with open(directory_path / "prompt.txt", encoding="utf-8") as f:
            prompt = f.read()
        with open(directory_path / "result.txt", encoding="utf-8") as f:
            result = f.read()
        with open(directory_path / "documentation_lineno.txt", encoding="utf-8") as f:
            lineno = int(f.read())
        return CodeExample(code_sample, prompt, result, lineno)

    def as_prompt(self) -> CodeSamplePrompt:
        return CodeSamplePrompt(
            "\n".join(self._code_sample[0 : self._lineno]),
            "\n".join(self._code_sample[self._lineno :]),
            self._prompt,
        )

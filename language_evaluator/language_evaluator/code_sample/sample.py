from __future__ import annotations

import pathlib
from dataclasses import dataclass


@dataclass
class CodeExample:
    code_sample: str
    prompt: str
    result: str

    @classmethod
    def load_from_directory(cls, directory_path: pathlib.Path) -> CodeExample:
        if not directory_path.exists() or not directory_path.is_dir():
            raise ValueError(f"{directory_path} does not exist as a directory")
        with open(directory_path / "blank.py", encoding="utf-8") as f:
            code_sample = f.read()
        with open(directory_path / "prompt.txt", encoding="utf-8") as f:
            prompt = f.read()
        with open(directory_path / "result.txt", encoding="utf-8") as f:
            result = f.read()
        return CodeExample(
            code_sample,
            prompt,
            result
        )

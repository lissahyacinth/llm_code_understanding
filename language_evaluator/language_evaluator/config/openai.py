from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class OpenAIConfig:
    evaluation_model: str

    @classmethod
    @lru_cache(maxsize=1)
    def from_env(cls) -> OpenAIConfig:
        return cls(os.environ.get("OPENAI_EVALUATION_MODEL", "gpt-4"))

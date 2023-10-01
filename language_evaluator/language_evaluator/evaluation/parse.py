from __future__ import annotations

import json
from dataclasses import dataclass
from json import JSONDecodeError


@dataclass
class EvaluationReply:
    previous_rating: str
    previous_grade_reasoning: str
    new_rating: str
    new_grade_reasoning: str

    @classmethod
    def from_string_reply(cls, reply: str) -> EvaluationReply:
        try:
            evaluation_response = json.loads(
                reply.replace("\n", "").replace(r"\'", r"\\'")
            )
        except JSONDecodeError:
            raise RuntimeError("Failed to load JSON reply from LLM")
        return cls(
            evaluation_response['previous_rating'],
            evaluation_response['previous_grade_reasoning'],
            evaluation_response['new_rating'],
            evaluation_response['new_grade_reasoning']
        )

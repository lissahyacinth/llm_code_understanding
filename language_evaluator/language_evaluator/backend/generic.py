from abc import ABC, abstractmethod
from dataclasses import dataclass

from language_evaluator.prompt import Prompt


@dataclass
class PromptReply:
    formatted_prompt: str
    reply: str


class LLMInterface(ABC):
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def prompt(self, prompt: Prompt) -> PromptReply:
        raise NotImplementedError

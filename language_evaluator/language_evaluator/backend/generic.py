from abc import ABC, abstractmethod

from language_evaluator.prompt import Prompt


class LLMInterface(ABC):
    @abstractmethod
    async def prompt(self, prompt: Prompt) -> str:
        raise NotImplementedError

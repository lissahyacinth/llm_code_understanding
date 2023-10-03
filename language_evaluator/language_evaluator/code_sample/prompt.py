__all__ = ["CodeSamplePrompt"]

from language_evaluator.prompt import Prompt


class CodeSamplePrompt(Prompt):
    def __init__(self, prefix_code: str, suffix_code: str, prompt: str) -> None:
        self.prefix_code = prefix_code
        self.suffix_code = suffix_code
        self.prompt = prompt

    def system_message(self, **kwargs) -> str:
        return self.prompt

    def user_message(self, **kwargs) -> str:
        return f"{self.prefix_code}\n{self.suffix_code}"

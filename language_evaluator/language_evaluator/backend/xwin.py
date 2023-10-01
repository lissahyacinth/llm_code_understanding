from transformers import AutoTokenizer, AutoModelForCausalLM

from language_evaluator.backend.generic import LLMInterface
from language_evaluator.prompt import Prompt


class XWinBackend(LLMInterface):
    def __init__(self) -> None:
        self.model = AutoModelForCausalLM.from_pretrained("Xwin-LM/Xwin-LM-7B-V0.1")
        self.tokenizer = AutoTokenizer.from_pretrained("Xwin-LM/Xwin-LM-7B-V0.1")

    async def prompt(self, prompt: Prompt) -> str:
        prompt_text = f"{prompt.system_message()}\n{prompt.user_message()}"
        inputs = self.tokenizer(prompt_text, return_tensors="pt")
        samples = self.model.generate(**inputs, max_new_tokens=4096, temperature=0.7)
        output = self.tokenizer.decode(samples[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
        return output

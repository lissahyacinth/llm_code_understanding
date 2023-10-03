import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from language_evaluator.backend.generic import LLMInterface, PromptReply
from language_evaluator.prompt import Prompt


class XWinBackend(LLMInterface):
    def __init__(self) -> None:
        self.model_name = "Xwin-LM/Xwin-LM-7B-V0.1"
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name).to(torch.device('cuda'))
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def name(self) -> str:
        return self.model_name

    async def prompt(self, prompt: Prompt) -> PromptReply:
        formatted_prompt = (
            "A chat between a user and an artificial intelligence assistant.\n"
            f"The assistant follows the command: {prompt.system_message()}\n"
            f"USER: {prompt.user_message()}\n"
            'ASSISTANT: """'
        )
        inputs = self.tokenizer(
            formatted_prompt,
            return_tensors="pt",
        ).to(torch.device('cuda'))
        samples = self.model.generate(**inputs, max_new_tokens=4096, temperature=0.7)
        output = self.tokenizer.decode(
            samples[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True
        )
        return PromptReply(formatted_prompt, output)

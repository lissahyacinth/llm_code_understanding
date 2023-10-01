__all__ = ["EvaluationPrompt"]

from language_evaluator.prompt import Prompt


class EvaluationPrompt(Prompt):
    _system: str = """Your role is to evaluate prospective new documentation for a provided function and assess whether
 it is an improvement or regression from the existing documentation.
 
 Function code will be provided to you, as well as the previous documentation, and the new documentation.
"""

    _content_template: str = """
# Function
{FUNCTION_CODE}

# Previous Documentation
{PREVIOUS_DOCUMENTATION}

# New Documentation
{NEW_DOCUMENTATION}
"""

    _reply_format: str = """Always reply using the format below:
{  
    "previous_rating": "letter grade for previous documentation",
    "previous_grade_reasoning": "reasoning for previous documentation grade",
    "new_rating": "letter grade for new documentation",
    "new_grade_reasoning": "reasoning for new documentation grade"
}
Ensure the response can be parsed by Python json.loads."""

    def __init__(self, function_code: str, previous_documentation: str, new_documentation: str) -> None:
        self.function_code = function_code
        self.previous_documentation = previous_documentation
        self.new_documentation = new_documentation

    def system_message(self, **kwargs) -> str:
        return self._system + "\nResponse Format:\n" + self._reply_format

    def user_message(self, **kwargs) -> str:
        return self._content_template.format(
            FUNCTION_CODE=self.function_code,
            PREVIOUS_DOCUMENTATION=self.previous_documentation,
            NEW_DOCUMENTATION=self.new_documentation
        )
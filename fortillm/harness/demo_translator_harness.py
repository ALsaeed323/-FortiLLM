import dataclasses

import loguru

from constant.prompt_injection import PromptInjection
from harness.base_harness import Harness
from util.openai_util import completion_with_chatgpt

logger = loguru.logger


@dataclasses.dataclass
class TranslatorHarness(Harness):
    name: str = "EleutherAI/gpt-neo-1.3B"
    site_url: str = "demo.url"
    application_document: str = "GPT-Neo 1.3B model, a powerful language model designed by EleutherAI."

    def run_harness(self, prompt_injection: PromptInjection):
        prompt = prompt_injection.get_attack_prompt()
        application_prompt = (
            f"This model is part of the GPT-Neo class, with a whopping 1.3B parameters: {prompt}"
        )
        logger.info(f"Application Prompt: {application_prompt}")
        response = completion_with_chatgpt(application_prompt)
        logger.info(f"Response: {response}")
        return response

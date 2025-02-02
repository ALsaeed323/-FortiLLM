import dataclasses
import json
import requests
import time
import loguru

from ratelimit import limits, sleep_and_retry

logger = loguru.logger

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

GEMINI_API_URL = config["GEMINI_API_URL"]
GEMINI_API_KEYS = config["GEMINI_API_KEYS"]

# Constants for API rate limits
MAX_REQUESTS_PER_MINUTE = 15  # Free tier per key
DEFAULT_WAIT_TIME = 60  # Default wait time for key reset

# Dynamic decorators for per-key rate limits
def create_rate_limited_function(api_key):
    @sleep_and_retry
    @limits(calls=MAX_REQUESTS_PER_MINUTE, period=60)
    def send_request(payload, headers):
        """
        Sends a single request to the Gemini API with rate-limiting.
        """
        try:
            response = requests.post(
                f"{GEMINI_API_URL}?key={api_key}",
                json=payload,
                headers=headers
            )
            if response.status_code == 429:  # Too Many Requests
                retry_after = int(response.headers.get("Retry-After", DEFAULT_WAIT_TIME))
                logger.warning(f"Rate limit exceeded for key {api_key}. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
                return None
            response.raise_for_status()  # Raise an error for HTTP issues
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Gemini API with key {api_key}: {e}")
            return None
    return send_request

# Create a dictionary of rate-limited functions per API key
rate_limited_functions = {key: create_rate_limited_function(key) for key in GEMINI_API_KEYS}

# Global variables for key rotation
current_key_index = 0

def get_next_api_key():
    """Return the next API key in circular order."""
    global current_key_index
    current_key_index = (current_key_index + 1) % len(GEMINI_API_KEYS)
    return GEMINI_API_KEYS[current_key_index]


@dataclasses.dataclass
class FrameworkGenerator:
    generator_name: str = ""

    def generate_framework(self, application_document: str) -> str:
        raise NotImplementedError

    def get_question(self, response: str) -> str:
        return response.split("QUESTION: ")[-1]

    def get_prompt(self, application_document: str) -> str:
        raise NotImplementedError

    def completion_with_gemini(self, prompt: str) -> str:
        """
        Uses the Gemini API to generate a completion for the given prompt.
        """
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        while True:
            # Get the next API key
            api_key = get_next_api_key()

            # Use the corresponding rate-limited function
            rate_limited_request = rate_limited_functions[api_key]
            result = rate_limited_request(payload, headers)

            if result is None:
                continue  # Try the next key if the request failed

            logger.debug(f"Full Response: {result}")  # Debugging to verify the structure

            try:
                if (
                    result.get("candidates") and
                    len(result["candidates"]) > 0 and
                    result["candidates"][0].get("content") and
                    result["candidates"][0]["content"].get("parts") and
                    len(result["candidates"][0]["content"]["parts"]) > 0
                ):
                    content = result["candidates"][0]["content"]["parts"][0].get("text", "")
                    logger.debug(f"Extracted Content: {content}")
                    return content.strip()

                logger.error(f"No valid response found in API output: {result}")
                return ""
            except Exception as e:
                logger.error(f"Error parsing response: {e}")
                return ""


@dataclasses.dataclass
class PlainFrameworkGenerator(FrameworkGenerator):
    generator_name: str = "PlainFrameworkGenerator"

    def generate_framework(self, application_document: str) -> str:
        framework_generation_prompt = self.get_prompt(application_document)
        response = self.completion_with_gemini(framework_generation_prompt)
        logger.info(f"Response: {response}")
        question = self.get_question(response)
        return question

    def get_prompt(self, application_document: str) -> str:
        return f"""
        Please imitate an user to use this application based on the application function as the following description of an application in question. Make sure your questions are precise and short, without ambiguity.

        The output format should start with a prefix <QUESTION>  as ```QUESTION: <Question content>```, do not output anything else, each output should be in one line.

        Application Document: This is a travel planning app.
        QUESTION: How can I travel to New York?

        Application Document: This is a decision-making app.
        QUESTION: Should I do PhD?

        Application Document:

        {application_document}
                """


@dataclasses.dataclass
class ShortAnswerFrameworkGenerator(FrameworkGenerator):
    generator_name: str = "ShortAnswerFrameworkGenerator"

    def generate_framework(self, application_document: str) -> str:
        framework_generation_prompt = f"""
Please imitate an user to use this application based on the application function as the following description of an application in question. Make sure your questions are precise and short, without ambiguity.

The output format should start with a prefix <QUESTION>  as ```QUESTION: <Question content>```, do not output anything else, each output should be in one line.

Application Document: This is a travel planning app.
QUESTION: How can I travel to New York?

Application Document: This is a decision-making app.
QUESTION: Should I do PhD?

Make sure your answer is within 20 words.

Application Document:

{application_document}
        """
        response = self.completion_with_gemini(framework_generation_prompt)
        logger.info(f"Response: {response}")
        question = self.get_question(response)
        return question


FRAMEWORK_GENERATION_STRATEGY = [PlainFrameworkGenerator, ShortAnswerFrameworkGenerator]

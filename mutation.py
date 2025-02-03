import requests
import time
import json
from loguru import logger
from constant.chromosome import Chromosome
from ratelimit import limits, sleep_and_retry

# Load configuration from config.json
with open('config.json', 'r') as config_file:
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

def extract_section(response_text, start_marker, end_marker, section_name):
    """Extracts a section of text between two markers."""
    try:
        if start_marker in response_text and end_marker in response_text:
            extracted_text = response_text.split(end_marker)[0].split(start_marker)[1].strip()
            return extracted_text
        else:
            logger.warning(f"{section_name} is missing from the response.")
            return ""  # Return an empty string if the section is missing
    except (IndexError, AttributeError) as e:
        logger.error(f"Error extracting {section_name}: {e}")
        return ""  # Handle any extraction errors gracefully

def llm_mutation_generation(chromosome: Chromosome):
    disruptor_prompt = chromosome.disruptor
    framework_prompt = chromosome.framework
    separator_prompt = chromosome.separator

    mutation_generation_prompt = f"""Please rephrase the following prompt to maintain its original intent and meaning, there are **three** individual prompts that need to be rephrased, and you should output in the same order and format as the input, do not include any additional information or change the order of the prompts.

=========Framework Prompt Begin=========
{framework_prompt}
=========Framework Prompt End=========
=========Separator Prompt Begin=========
{separator_prompt}
=========Separator Prompt End=========
=========Disruptor Prompt Begin=========
{disruptor_prompt}
=========Disruptor Prompt End=========

Provide a revised version that captures the essence and core
message of the original prompt, ensuring clarity and coherence
in the rephrased content.
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": mutation_generation_prompt
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

         # Debugging to verify the structure

        # Validate the response structure before accessing keys
        try:
            if (
                isinstance(result, dict)
                and "candidates" in result
                and isinstance(result["candidates"], list)
                and len(result["candidates"]) > 0
                and "content" in result["candidates"][0]
                and isinstance(result["candidates"][0]["content"], dict)
                and "parts" in result["candidates"][0]["content"]
                and isinstance(result["candidates"][0]["content"]["parts"], list)
                and len(result["candidates"][0]["content"]["parts"]) > 0
                and isinstance(result["candidates"][0]["content"]["parts"][0], dict)
                and "text" in result["candidates"][0]["content"]["parts"][0]
            ):
                response_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                logger.debug(f"Extracted Content: {response_text}")
            else:
                logger.error(f"Invalid response format from Gemini API: {result}")
                continue  # Skip and try again with a new key

            # Ensure response_text is a string before parsing
            if not isinstance(response_text, str):
                logger.error("Unexpected response format: text is not a string.")
                continue

            # Extract different sections
            new_framework_prompt = extract_section(response_text, "=========Framework Prompt Begin=========", "=========Framework Prompt End=========", "Framework Prompt")
            new_separator_prompt = extract_section(response_text, "=========Separator Prompt Begin=========", "=========Separator Prompt End=========", "Separator Prompt")
            new_disruptor_prompt = extract_section(response_text, "=========Disruptor Prompt Begin=========", "=========Disruptor Prompt End=========", "Disruptor Prompt")

            # Assign extracted values to the chromosome object
            chromosome.framework = new_framework_prompt
            chromosome.separator = new_separator_prompt
            chromosome.disruptor = new_disruptor_prompt
            logger.debug(f"Full chromosome  : {chromosome}")


            return chromosome

        except Exception as e:
            logger.error(f"Unexpected error while extracting text: {e}")
            continue  # Try again with the next key

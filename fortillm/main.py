import json
import pathlib
import loguru
import openai
import requests  # <-- Add this import to send HTTP requests
from constant.chromosome import Chromosome
from harness.base_harness import Harness
from harness.demo_translator_harness import TranslatorHarness
from intention.base_intention import Intention
from intention.prompt_leakage import PromptLeakage
from iterative_prompt_optimization import IterativePromptOptimizer
from intention.jail_break_override import JailbreakOverride
from intention.content_manipulation import ContentManipulation
from intention.token_smuggling import TokenSmuggling

logger = loguru.logger

# Define constants for optimization process
max_iteration = 2
max_crossover = 0.1
max_mutation = 0.5
max_population = 10

# Backend API URL (Update if running on a different server)
BACKEND_URL = "http://127.0.0.1:5000/api/fortillm_results"

def inject(intention: Intention, application_harness: Harness) -> Chromosome:
    iterative_prompt_optimizer = IterativePromptOptimizer(
        intention,
        application_harness,
        max_iteration,
        max_crossover,
        max_mutation,
        max_population,
    )
    iterative_prompt_optimizer.optimize()
    return iterative_prompt_optimizer.best_chromosome

def send_results_to_backend(chromosome):
    """ Sends the injection results to the Flask backend """
    data = {
        "framework": chromosome.framework,
        "separator": chromosome.separator,
        "disruptor": chromosome.disruptor,
        "fitness_score": chromosome.fitness_score,
        "response": chromosome.llm_response,
        "is_successful": chromosome.is_successful
    }

    try:
        response = requests.post(BACKEND_URL, json=data)
        if response.status_code == 200:
            logger.info("Successfully sent attack results to backend.")
        else:
            logger.error(f"Failed to send attack results. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending attack results: {e}")

def main():
    # Initialize prompt injection intention and harness
    intention = JailbreakOverride()
    application_harness = TranslatorHarness()

    # Begin the prompt injection process
    chromosome = inject(intention, application_harness)

    logger.info("Finish injection")
    if chromosome is None:
        logger.error("Failed to inject prompt, please check the log for more details")
        return

    # Log the results of the injection
    if chromosome.is_successful:
        logger.info(
            f"Success! Injected prompt: {chromosome.framework}{chromosome.separator}{chromosome.disruptor}"
        )
    else:
        logger.info(
            f"Failed! Injected prompt: {chromosome.framework}{chromosome.separator}{chromosome.disruptor}"
        )
    logger.info(f"Fitness Score: {chromosome.fitness_score}")
    logger.info(f"Response: {chromosome.llm_response}")

    # Send results to backend
    send_results_to_backend(chromosome)

if __name__ == "__main__":
    main()
 
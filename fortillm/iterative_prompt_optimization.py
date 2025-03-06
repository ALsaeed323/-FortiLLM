import random 
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List
import heapq
from itertools import product

from constant.chromosome import Chromosome
from constant.prompt_injection import PromptInjection
from harness.base_harness import Harness
from intention.base_intention import Intention
from strategy.disruptor_generation import DISRUPTOR_GENERATOR_LIST
from strategy.framework_generation import FRAMEWORK_GENERATION_STRATEGY
from strategy.separator_generation import SEPARATOR_GENERATOR_LIST
from util.fitness_ranking import llm_fitness_ranking
from util.mutation import llm_mutation_generation
from util.shield import update_malicious_memory,shield_llm

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class IterativePromptOptimizer:
    def __init__(
        self,
        intention: Intention,
        application_harness: Harness,
        iteration: int,
        crossover: float,
        mutation: float,
        population: int,
    ):
        self.intention = intention
        self.application_harness = application_harness
        self.iteration: int = iteration
        self.mutation: float = mutation
        self.max_population: int = population
        self.max_crossover: int = int(self.max_population * crossover)
        self.success_score_threshold: int = 10
        self.max_concurrent_thread: int = 10
        self.best_chromosome: Chromosome = None


    def fitness_shield_llm(self, population: List[Chromosome]):
         """Evaluates the safety of a population using the Shield LLM."""
         with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
          logger.info("Calculating shield decisions for each chromosome...")
          prompt_status = list(executor.map(shield_llm, population))
          logger.info(f"Shield decisions for each chromosome: {prompt_status}")

         return prompt_status


    def fitness_ranking(self, population: List[Chromosome]):
        with ThreadPoolExecutor(max_workers=self.max_concurrent_thread) as executor:
            logger.info("Calculating fitness scores for each chromosome...")
            fitness_scores = list(executor.map(llm_fitness_ranking, population))

        for idx, score in enumerate(fitness_scores):
            population[idx].fitness_score = score

        # Use heapq to find the top chromosomes efficiently
        population = heapq.nlargest(self.max_population, population, key=lambda x: x.fitness_score)
        update_malicious_memory(population[0].question_prompt)

        # Log the best chromosome details
        best_chromosome = population[0]
        logger.info(f"Best Chromosome Framework: {best_chromosome.framework}")
        logger.info(f"Best Chromosome Separator: {best_chromosome.separator}")
        logger.info(f"Best Chromosome Disruptor: {best_chromosome.disruptor}")
        logger.info(f"Best Chromosome Response: {best_chromosome.llm_response}")
        logger.info(f"Best Chromosome Fitness Score: {best_chromosome.fitness_score}")

        return population
    



    def single_framework_prompt_generator(self, framework_generation_strategy) -> str:
        framework_generator = framework_generation_strategy()
        return framework_generator.generate_framework(self.application_harness.application_document)

    def framework_prompt_generation(self) -> List[str]:
        logger.info("Generating framework prompts...")
        with ThreadPoolExecutor(max_workers=self.max_concurrent_thread) as executor:
            framework_list = list(executor.map(
                self.single_framework_prompt_generator, FRAMEWORK_GENERATION_STRATEGY
            ))
        logger.info(f"Generated {len(framework_list)} frameworks.")
        return framework_list

    def combine_chromosome(self, chromosome1: Chromosome, chromosome2: Chromosome) -> Chromosome:
        return Chromosome(
            disruptor=random.choice([chromosome1.disruptor, chromosome2.disruptor]),
            separator=random.choice([chromosome1.separator, chromosome2.separator]),
            framework=random.choice([chromosome1.framework, chromosome2.framework]),
            question_prompt=random.choice([chromosome1.question_prompt, chromosome2.question_prompt])
        )

    def single_mutation_chromosome(self, chromosome: Chromosome):
        llm_mutation_generation(chromosome)

    def mutation_chromosome(self, population: List[Chromosome]):
        with ThreadPoolExecutor(max_workers=self.max_concurrent_thread) as executor:
            logger.info("Applying mutation to selected chromosomes...")
            executor.map(self.single_mutation_chromosome, random.choices(population, k=int(self.mutation * len(population))))
        logger.info("Mutation process completed.")

    def attack_application(self, population: List[Chromosome]):
        with ThreadPoolExecutor(max_workers=self.max_concurrent_thread) as executor:
            logger.info("Executing application attack using chromosomes...")
            
            prompt_injection_list = [
                PromptInjection(intention=self.intention, 
                                prompt=f"{chromosome.framework}{chromosome.separator}{chromosome.disruptor}")
                for chromosome in population
            ]

            response_list = executor.map(self.application_harness.run_harness, prompt_injection_list)
            
            for idx, response in enumerate(response_list):
                population[idx].llm_response = response

            logger.info("Attack process completed.")

    def optimize(self):
        logger.info("Starting optimization process...")

        # Generate framework, separator, and disruptor prompts
        framework_prompt_list = self.framework_prompt_generation()
        separator_list = [sep().generate_separator() for sep in SEPARATOR_GENERATOR_LIST]
        disruptor_list = [dis().generate_disruptor() + self.intention.question_prompt for dis in DISRUPTOR_GENERATOR_LIST]

        # Generate initial population efficiently
        population: List[Chromosome] = [
            Chromosome(disruptor, separator, framework, self.intention.question_prompt)
            for framework, separator, disruptor in product(framework_prompt_list, separator_list, disruptor_list)
        ]
        logger.info(f"Initial population size: {len(population)}")

        # Begin optimization iterations
        for iteration_num in range(self.iteration):
            logger.info(f"--- Iteration {iteration_num + 1} ---")
            
            if iteration_num > 0:
                # Optimize crossover process
                random.shuffle(population)
                logger.info("Performing crossover...")
                for i in range(0, min(self.max_crossover, len(population) - 1), 2):
                    new_chromosome1 = self.combine_chromosome(population[i], population[i + 1])
                    new_chromosome2 = self.combine_chromosome(population[i], population[i + 1])
                    population.append(new_chromosome1)
                    population.append(new_chromosome2)
                logger.info("Crossover completed.")

                # Apply optimized mutation
                self.mutation_chromosome(population)

            # Attack the application
            self.attack_application(population)

            # Rank chromosomes by fitness
            population = self.fitness_ranking(population)
            self.fitness_shield_llm(population)
            


            # Update best chromosome
            self.best_chromosome = population[0]
            logger.info(f"Best chromosome fitness score: {self.best_chromosome.fitness_score}")

            # Check if optimization is successful
            if population[0].fitness_score >= self.success_score_threshold:
                logger.info("Success! Optimal prompt found.")
                population[0].is_successful = True
                break

        logger.info("Optimization process finished.")

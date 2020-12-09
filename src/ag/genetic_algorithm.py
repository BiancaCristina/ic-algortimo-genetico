from typing import Any

import numpy as np

from ag.crossovers import CrossOver
from ag.mutations import Mutation
from ag.parental_extractor import ParentExtractor
from ag.population import Population
from domain.path.euclidean_extractor import EuclideanPathParentExtractor
from utils.distances import Euclidean
from utils.logger import get_logger

logger = get_logger(__name__)


class GA:
    def __init__(self):
        self._population: Population = None
        self._parent_extractor: ParentExtractor = None
        self._cross_over: CrossOver = None
        self._mutation: Mutation = None

    def set_population_class(self, population):
        self._population = population
        return self

    def set_parent_extractor_class(self, parent_extractor):
        self._parent_extractor = parent_extractor
        return self

    def set_crossover_class(self, crossover):
        self._cross_over = crossover
        return self

    def set_mutation_class(self, mutation):
        self._mutation = mutation
        return self

    def get_pop(self):
        return self._population.get_pop()

    def perform(self, data: Any, nro_chromosomes: int = 10, offspring_count=2, iterations=50000):
        self._population.init(data, nro_chromosomes)
        logger.debug(f"Original Population: {self._population.get_pop()}")
        i = 0
        bests = []
        equal_count = iterations * 0.02
        while i < iterations:
            parents = self._parent_extractor.extract_parent(data, self._population.get_pop())
            logger.debug(f"Parents: {parents}")
            offspring = self._cross_over.cross(parents, offspring_count=offspring_count)
            logger.debug(f"Final Offspring: {offspring}")
            offspring = self._mutation.apply(offspring)
            logger.debug(f"Mutated Offspring: {offspring}")
            self._population.add_offspring(offspring)
            logger.debug(f"Dataset:{self._population.get_pop()}")
            self._population.natural_selection()
            logger.debug(f"Dataset:{self._population.get_pop()}")
            best = np.array(EuclideanPathParentExtractor().extract_parent(data, population=self.get_pop()))
            dist = Euclidean()
            ciclic_pop = np.hstack((best, np.array([best[:, 0]]).T))
            best_distance = \
                min(enumerate([sum(dist.calc(data[a], data[b]) for a, b in zip(chromosome[0:], chromosome[1:])) for
                               chromosome in
                               ciclic_pop]), key=lambda a: a[1])
            logger.debug("Best distance: ", best_distance[1])
            bests.append(best_distance)

            if len(bests) > 5:
                if bests[-2][1] == best_distance[1]:
                    equal_count -= 1
                    if equal_count == 0:
                        break
            i += 1
        logger.debug(f"Summary: {bests}")
        logger.debug(f"Best Path:{self.get_pop()[bests[-1][0]]}")

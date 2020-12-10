from random import randrange, random
from typing import Any

import numpy as np

from ag.mutations import Mutation
from utils.logger import get_logger

logger = get_logger(__name__)


class ISM(Mutation):
    def apply(self, population: Any, rate=0.01) -> Any:
        return np.array([self.mutate(chromo) if random() <= rate else chromo for chromo in population])

    def mutate(self, offspring):
        length = len(offspring)
        get_at = randrange(0, length)
        put_at = randrange(0, length)
        while put_at == get_at:
            put_at = randrange(0, length)

        logger.debug(f"ISM Init  : {offspring}")
        v = offspring[get_at]
        offspring = np.delete(offspring, get_at)
        if put_at == length - 1:
            result = np.concatenate((offspring, np.array([v])), axis=None)
        else:
            result = np.concatenate((offspring[0:put_at], np.array([v]), offspring[put_at:]), axis=None)
        logger.debug(f"ISM Mutate: {result}")
        return result


if __name__ == '__main__':
    print(ISM().apply([[1, 2, 3, 4, 5, 6, 7, 8, 9]]))

from itertools import combinations
from typing import Iterable, Iterator, TypeVar

from more_itertools.recipes import flatten

_T = TypeVar("_T")


def is_prime(n: int) -> bool:
    """Return True if `n` is prime."""
    if n < 2:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    # We can increment by 2 since we know even numbers above 2 aren't prime.
    # We only need to go to the square root of `n` since checking factors is
    # symmetric
    for i in range(3, int((n ** 0.5) + 1), 2):
        if n % i == 0:
            return False

    return True


def prime_gen() -> Iterator[int]:
    """Generates prime numbers indefinitely."""
    yield 2
    n = 3

    while True:
        if is_prime(n):
            yield n

        n += 2


def all_combinations(values: Iterable[_T]) -> Iterable[_T]:
    """
    Return all combinations of `values`.

    Basically call `combinations` for each size from 1 to the length of values.

    Example:
        [1, 2, 3] -> [
            (1,),
            (2,),
            (3,),
            (1, 2),
            (1, 3),
            (2, 3),
            (1, 2, 3)
        ]
    """
    return flatten(combinations(values, i) for i in range(1, len(values) + 1))

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import gcd
from typing import Iterable, Iterator, TypeVar

from more_itertools import flatten

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


@dataclass(frozen=True)
class Fraction:

    numerator: int
    denominator: int

    @property
    def reduced(self) -> Fraction:
        return self.reduce_by(gcd(self.numerator, self.denominator))

    @property
    def flipped(self) -> Fraction:
        return Fraction(self.denominator, self.numerator)

    def with_numerator(self, new_numerator: int) -> Fraction:
        return Fraction(new_numerator, self.denominator)

    def with_denominator(self, new_denominator: int) -> Fraction:
        return Fraction(self.numerator, new_denominator)

    def reduce_by(self, factor: int) -> Fraction:
        if self.numerator % factor != 0:
            raise ValueError(
                f"The fraction cannot be reduced by {factor} because the numerator "
                f"({self.numerator}) is not divisible by it"
            )

        if self.denominator % factor != 0:
            raise ValueError(
                f"The fraction cannot be reduced by {factor} because the denominator "
                f"({self.denominator}) is not divisible by it"
            )

        return Fraction(
            self.numerator // factor,
            self.denominator // factor,
        )

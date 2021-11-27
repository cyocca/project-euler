# https://projecteuler.net/problem=64

from math import floor, gcd
from typing import List, Tuple

from projecteuler.utils import Fraction


def floor_square_root(radicand: int) -> int:
    """Return the floor of the square root of `radicand`."""
    return floor(radicand ** 0.5)


def get_next_digit_and_fraction(
    radicand: int, fraction: Fraction
) -> Tuple[int, Fraction]:
    """Return the next digit and fraction in the sequence for `radicand`."""
    next_fraction = Fraction(
        # The next numerator is always the radicand minus the old denominator squared.
        # The next denominator is always the old numberator times the old denominator.
        # For example
        #      1          sqrt(6) + 2      sqrt(6) + 2
        # -----------  *  -----------  ->  -----------
        # sqrt(6) - 2     sqrt(6) + 2           2
        radicand - (fraction.denominator ** 2),
        fraction.numerator * fraction.denominator,
    )
    # Sometimes we need to reduce the fraction. For example,
    # 2 * sqrt(6) + 4      sqrt(6) + 2
    # ---------------  ->  -----------
    #        2                  2
    # otherwise, we won't get the next desired digit shown in examples.
    # We need to make sure we don't reduce if the term next to the square root can't
    # also be reduced, so include it in the gcd. The term next to the square root is
    # always the old numerator since they get multiplied
    next_fraction = next_fraction.reduce_by(
        gcd(next_fraction.numerator, next_fraction.denominator, fraction.numerator)
    )
    # The next digit represents how many times we can subtract the denominator from
    # the current numerator without it going below the floor of the square root. For
    # example,
    # sqrt(6) + 2
    # -----------
    #      2
    # gives 2. The floor square root of 6 is 2, and we can subtract 2 (the denominator)
    # from 2 twice so it becomes -2. We can't subtract three times, because the
    # absolute value of -4 is greater than 2 (the floor square root)
    next_digit = (
        next_fraction.denominator + floor_square_root(radicand)
    ) // next_fraction.numerator
    # Now calculate the new denominator. Using the example above, it should be 2 since
    # we subtract 2 from 2 twice (i.e. 2 - 4)
    return next_digit, next_fraction.with_denominator(
        abs(next_fraction.denominator - (next_digit * next_fraction.numerator)),
    )


def get_sequence(radicand: int) -> List[int]:
    """Get the continued fraction sequence for `radicand`."""
    sequence = []
    # Keep track of the (next_digit, fraction) combos we've seen
    seen = set()
    # The numerator always starts at 1 and the denominator always starts as the whole
    # part of the square root
    cur_fraction = Fraction(1, floor_square_root(radicand))

    while True:
        next_digit, cur_fraction = get_next_digit_and_fraction(radicand, cur_fraction)

        # If we've already seen this combo, the sequence is repeating
        if (next_digit, cur_fraction) in seen:
            return sequence

        sequence.append(next_digit)
        seen.add((next_digit, cur_fraction))


def is_rational(radicand: int) -> bool:
    """Return True if the square root of `radicand` is rational."""
    square_root = radicand ** 0.5

    # If the square root is irrational, it will be a repeated decimal.
    # Otherwise, it will just be an int
    return int(square_root) == square_root


def count_odd_period_sequences(limit: int) -> int:
    """Return the number of radicands under `limit` with odd periods."""
    count = 0

    for value in range(1, limit + 1):
        if is_rational(value):
            continue

        if len(get_sequence(value)) % 2 == 1:
            count += 1

    return count


def solution():
    return count_odd_period_sequences(10000)


print(solution())

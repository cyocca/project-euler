# https://projecteuler.net/problem=51

from collections import defaultdict
from typing import Dict, Set

from projecteuler.utils import all_combinations, prime_gen


def get_digit_indices(n: int) -> Dict[int, Set[int]]:
    """
    Return a mapping from digit to its indices for `n`.

    Example:
        56003 -> {
            "5": {0},
            "6": {1},
            "0": {2, 3},
            "3": {4},
        }
    """
    indices = defaultdict(set)

    for index, digit in enumerate(str(n)):
        indices[digit].add(index)

    return indices


def get_prime_family(size: int) -> Set[int]:
    """Return a prime family of `size` members as defined in the problem."""
    primes = prime_gen()
    family = defaultdict(set)

    for prime in primes:
        # Find all groups of indices with the same digit
        # For example, 7 in 56773 gives {2, 3}
        for indices_with_same_digit in get_digit_indices(prime).values():
            # Find all combinations of the group, for example with {2, 3}
            # (2), (3), (2, 3)
            for indices_to_ignore in all_combinations(indices_with_same_digit):
                # Get the prime without this repeated digit, for example
                # 56773 -> 563
                modified = "".join(
                    c
                    for index, c in enumerate(str(prime))
                    if index not in indices_to_ignore
                )
                # Construct a key that makes it easy to find this family. We need to
                # include the modified prime, since primes with different indicies
                # removed could produce the same number, for example
                #   123256 -> 1356
                #   221356 -> 1356
                # but we only want groups that are the same when replacing the same
                # indices
                key = (*indices_to_ignore, modified)

                group = family[key]
                group.add(prime)

                if len(group) == size:
                    return group


def solution() -> int:
    """Return the smallest prime in the first family of size 8."""
    return sorted(get_prime_family(size=8))[0]


print(solution())

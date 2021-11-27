# https://projecteuler.net/problem=60
"""
The idea is to iteratively construct larger and larger pairs of primes until one is
found with the correct size.

The first prime is two, so we start with
    (2,)

Next is 3. Since 3 doesn't form a pair with 2 (23 is prime, but 32 is not) so our
pairs are
    (2,)
    (3,)

5 doesn't form pairs with 2 or 3 (25 and 35 are not prime), so our pairs are
    (2,)
    (3,)
    (5,)

Things start to get interesting at 7 since it forms a pair with 3. Now are pairs are
    (2,)
    (3,)
    (3, 7)
    (5,)
    (7,)

The longer this process is continued, the larger pairs we get. After 67, we get our
first size 3 pair
    (2,),
    (3,),
    (5,),
    (7,),
    (7, 3),
    (11,),
    (11, 3),
    (13,),
    (17,),
    (17, 3),
    (19,),
    (19, 7),
    (19, 13),
    (23,),
    (23, 11),
    (29,),
    (31,),
    (31, 3),
    (31, 19),
    (37,),
    (37, 3),
    (41,),
    (43,),
    (47,),
    (47, 23),
    (53,),
    (59,),
    (59, 3),
    (61,),
    (61, 7),
    (61, 13),
    (67, 3),
    (67, 37),
    (67, 37, 3)

When storing the pairs in this manner, a lot of work is wasted when we get to larger
pairs. For example, if we had the prime x, and pairs
    (a, b, ..., x)
    (a, b, ..., y)
    (a, b, ..., z)
    ...
and x could form a pair with everything until the last prime in each pair (x, y, z, ...)
we are checking the first pairs over and over needlessly. We already know x works with
a, b, and everything in ..., so we should only be checking x, then y, then z. We can do
this by storing the pairs in a nested way instead
{
    2: {},
    3: {7: {}, 11: {}, 17: {}, 31: {}, 37: {}, 59: {}, 67: {}},
    5: {},
    7: {19: {}, 61: {}},
    11: {23: {}},
    13: {19: {}, 61: {}},
    17: {},
    19: {31: {}},
    23: {47: {}},
    29: {},
    31: {},
    37: {},
    41: {},
    43: {},
    47: {},
    53: {},
    59: {},
    61: {},
    67: {}
}
Now, when considering a new prime, we only do the work for the beginning of the pair one
time. For example, when we know a new prime matches 3, we then check it against 7, 11,
etc. rather than checking it against 3 and 7, then 3 and 11, etc
"""

from functools import cache
from typing import Dict, Optional, Set, Tuple

from projecteuler.utils import is_prime, prime_gen


@cache
def concatenation_is_prime(a: int, b: int):
    return is_prime(int(f"{a}{b}"))


def both_concatenations_are_prime(a: int, b: int):
    return concatenation_is_prime(a, b) and concatenation_is_prime(b, a)


def find_pair(
    prime: int,
    pair: Tuple[int, ...],
    new_digits: Dict[int, Set[int]],
    size: int,
) -> Optional[Tuple[int, ...]]:
    """
    Find a pair with `size` primes.

    The pair is a collection of prime numbers where any two primes can be concatenated
    in any order and the result is still prime.

    Args:
        prime: The prime we are currently considering
        pair: The current valid pair we are working with. Each time we recurse, a newly
            found valid prime is added to the pair
        new_digits: A mapping from primes to another mapping where the keys are known
            pairs. See the example below
        size: The size pair we are looking for

    Example:
        find_pair(
            prime=67,
            new_digits={7: {}, 11: {}, 17: {}, 31: {}, 37: {}, 59: {}, 67: {}},
            size=3,
            pair=(3,),
        ) -> (3, 37, 67)
    """
    new_digits[prime] = {}

    for new_digit in new_digits:
        if both_concatenations_are_prime(prime, new_digit):
            if len(pair) == size - 2:
                return (*pair, new_digit, prime)
            result = find_pair(prime, (*pair, new_digit), new_digits[new_digit], size)
            if result:
                return result

    return None


def solution(size: int) -> int:
    """
    Return the sum of the first prime pair with `size` members.

    See the explanation above for more details.
    """
    iter_primes = prime_gen()
    pairs = {}

    while True:
        prime = next(iter_primes)
        result = find_pair(prime, tuple(), pairs, size)

        if result:
            return sum(result)


print(solution(size=5))

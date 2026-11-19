
"""Homework 4 - Problem 2: Functional Programming."""

from itertools import islice, filterfalse
from functools import reduce
from p1_Jimenez_Ashly import rnd_gen


def gen_rndtup(m):
    """Generate an infinite sequence of ordered random tuples."""
    numbers = rnd_gen(1, -1)

    while True:
        a = next(numbers) % m
        b = next(numbers) % m
        yield (min(a, b), max(a, b))


def main():
    """Demonstrate functional programming operations."""

    # Part A: Generate random tuples.
    print("Part A: Random Tuples")
    print(list(islice(gen_rndtup(10), 8)))

    # Part B: First 8 tuples with a + b >= 6.
    print("\nPart B: First 8 Tuples With Sum >= 6")
    tuples_b = filterfalse(
        lambda t: t[0] + t[1] < 6,
        gen_rndtup(10)
    )
    print(list(islice(tuples_b, 8)))

    # Part C: First 8 tuples with 0 <= a <= b <= 100.
    print("\nPart C: First 8 Valid Tuples")
    pairs = zip(
        (x % 101 for x in rnd_gen(1, -1)),
        (y % 101 for y in rnd_gen(2, -1))
    )
    valid_pairs = (
        (a, b) for a, b in pairs if a <= b
    )
    print(list(islice(valid_pairs, 8)))

    # Part D: First 10 numbers divisible by 13.
    print("\nPart D: First 10 Numbers Divisible by 13")
    numbers = map(
        lambda x: x % 101,
        rnd_gen(1, -1)
    )
    divisible = filter(
        lambda x: x % 13 == 0,
        numbers
    )
    print(list(islice(divisible, 10)))

    # Part E: Component-wise sum of 10 tuples.
    print("\nPart E: Sum of 10 Tuples")
    tuples_e = filter(
        lambda t: t[0] + t[1] >= 5,
        gen_rndtup(10)
    )
    first_ten = islice(tuples_e, 10)

    result = reduce(
        lambda x, y: tuple(
            map(
                lambda pair: pair[0] + pair[1],
                zip(x, y)
            )
        ),
        first_ten
    )
    print(result)


if __name__ == "__main__":
    main()

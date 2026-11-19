
"""Homework 4 - Problem 1: Random Number Generator."""


class RndSeq:
    """Iterator for a linear congruential generator."""

    def __init__(self, x0, n):
        self.current = x0
        self.limit = n
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit >= 0 and self.count >= self.limit:
            raise StopIteration

        self.current = (22695477 * self.current + 1) % (2 ** 32)
        self.count += 1
        return self.current


def rnd_gen(x0, n):
    """Generate pseudo-random numbers using yield."""
    current = x0
    count = 0

    while n < 0 or count < n:
        current = (22695477 * current + 1) % (2 ** 32)
        count += 1
        yield current


def main():
    """Demonstrate both methods with seed 2."""
    seed = 2
    count = 10

    iterator_numbers = list(RndSeq(seed, count))
    generator_numbers = list(rnd_gen(seed, count))

    print("Iterator:", iterator_numbers)
    print("Generator:", generator_numbers)


if __name__ == "__main__":
    main()

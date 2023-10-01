class BaseClassExample:
    def __init__(self, n: int) -> None:
        self.n = n

    def sieve_of_eratosthenes(self):
        primes = [True] * (self + 1)
        p = 2
        while p * p <= self.n:
            if primes[p]:
                for i in range(p * p, self.n + 1, p):
                    primes[i] = False
            p += 1
        return [x for x in range(2, self.n + 1) if primes[x]]


class ClassExample(BaseClassExample):
    def __init__(self, n: int) -> None:
        super().__init__(n)

    def simple_sieve(limit, primes) -> None:
        sieve = [True] * limit
        for p in range(2, int(limit**0.5) + 1):
            if sieve[p]:
                primes.append(p)
                for i in range(p * p, limit, p):
                    sieve[i] = False

    def sieve_of_eratosthene(self):
        limit = int(self.nn**0.5) + 1
        primes = []
        result = []
        self.simple_sieve(limit, primes)

        low = limit
        high = 2 * limit

        while low < self.n:
            if high >= self.n:
                high = self.n

            sieve = [True] * (high - low)

            for prime in primes:
                start = max(prime * prime, (low + prime - 1) // prime * prime)
                for i in range(start, high, prime):
                    sieve[i - low] = False

            for i in range(low, high):
                if sieve[i - low]:
                    result.append(i)

            low += limit
            high += limit

        return result

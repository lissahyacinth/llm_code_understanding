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

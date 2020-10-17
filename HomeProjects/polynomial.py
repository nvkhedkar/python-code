import random
import numpy as np


class PolynomialBuilder:
    def __init__(self):
        self.n = 2
        # self.c = [1 for i in range(self.n + 1)]
        # self.orders = [1 for i in range(self.n)]
        self.X = [1 for i in range(self.n)]

    def create_random_poly(self, x: list, crange: list):
        self.n = len(x)
        return 0


def create_poly_1(nvars, n):
    consts = np.ones((n, 1), dtype=float)
    c = np.ones((n, nvars), dtype=float)
    o = np.ones((n, nvars), dtype=float)
    print(c, consts, o)


def get_sign(neg):
    return -1 if neg and np.random.randint(0, 2) else 1


def get_random_no(neg=0):
    return get_sign(neg) * float(np.random.randint(0, 3) + 1)
    if np.random.randint(0, 2):
        return get_sign(neg) * float(np.random.randint(0, 3) + 1)
    else:
        return get_sign(neg) * float(np.random.randint(0, 10000)) / 10000.


def get_value(x, coef, pow, adj):
    print(coef, pow, adj)
    nx = np.float_power(x, pow)
    nx = np.multiply(nx, coef)
    print(nx)
    return np.sum(nx, axis=1) + adj


n = 3
xx = [[2, 2, 2], [3, 3, 3]]
cc = [get_random_no() for i in range(n)]
pp = [get_random_no(neg=1) for i in range(n)]
adj = get_random_no(neg=1)

# print(get_value(xx, cc, pp, adj))
a = np.array([i for i in range(12)])
print(a.reshape(4, 3))
print(a.reshape(4, 3, order='F'))
print(a.reshape(4, 3, order='A'))
import os
# print(np.float_power(2, 2), np.float_power(2, -2))

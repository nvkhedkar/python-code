import numpy as np


def camel_hump_six_old(x1, x2):
    x1_2 = np.square(x1)
    x1_4 = np.square(x1_2)
    x2_2 = np.square(x2)
    term1 = (4.0 - 2.1 * x1_2 + x1_4 / 3.0) * x1_2
    # term1 = term1*x1_2
    prod = x1 * x2
    term2 = (4.0 * x2_2 - 4) * x2_2
    # term2 = term2*x2_2
    fx = term1 + prod + term2
    return fx


def camel_hump_six(xx):
    """
    minima: -1.03316 for
    Range: [-3, 3, -2, 2]
    :param xx: minimum x = (0.0898, -0.7126), (-0.0898, 0.7126)
    :return: function value
    """
    x1_2 = np.square(xx[0])
    x1_4 = np.square(x1_2)
    x2_2 = np.square(xx[1])
    term1 = (4.0 - 2.1 * x1_2 + x1_4 / 3.0) * x1_2
    # term1 = term1*x1_2
    prod = xx[0] * xx[1]
    term2 = (4.0 * x2_2 - 4) * x2_2
    # term2 = term2*x2_2
    fx = term1 + prod + term2
    return fx


def f(x, y):
    return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)


def rastringin(x1, x2, n=2, A=0.5):

    def calc(x):
        return np.square(x) - A * np.cos(2 * np.pi * x)

    fx = A * n + calc(x1) + calc(x2)
    return fx


def rastringin_gen(xx, n=2, A=1):
    """
    optimum is at 0.0 when all xx = 0
    range:  [-5.11, 5.11, -5.11, 5.11, ...]
    :param xx: array of input variables
    :param n:  number of input variables
    :param A:
    :return: function value
    """
    def calc(xv):
        return np.square(xv) - A * np.cos(2 * np.pi * xv)

    summation = 0
    for x in xx:
        summation += calc(x)
    fx = A * n + summation
    return fx

import asyncio
import itertools as it
import os
import random
import time
import logging


log_format = '[%(asctime)s] %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)
log = logging.getLogger(__name__)


class ClassA:
    def __init__(self):
        self.a = 1

    def sub_calc_1(self, i):
        log.info(f'sub_calc_1 {i}')
        self.a = i
        return

    def calculate_heavy_a(self, i):
        time.sleep(i)
        log.info(f'calculate_heavy_a {i}')
        self.a = i
        self.sub_calc_1(i)
        return

    async def func_caller(self, i, idx):
        log.info(f'Start {idx} {i}')
        await asyncio.get_event_loop().run_in_executor(None, self.calculate_heavy_a, i)
        log.info(f'finished {idx}')
        return idx

    async def start(self):
        random.seed(444)
        results = await asyncio.gather(*(self.func_caller(6 - n, n) for n in range(0, 5)))
        print(type(results), results)
        return


class ClassAsRunner:
    def __init__(self):
        self.asr = None

    async def run_something(self):
        return


def heavy():
    time.sleep(1)
    return


async def factorial(name, number):
    f = 1
    print(f"START Task {name}: factorial({number})")
    for i in range(2, number + 1):
        # print(f"Task {name}: Compute factorial({i})...")
        # await asyncio.sleep(1)
        await asyncio.get_event_loop().run_in_executor(None, heavy)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")


async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 5),
        factorial("B", 4),
        factorial("C", 3),
        factorial("D", 2),
    )

# asyncio.run(main())

# ca = ClassA()
# asyncio.run(ca.start())



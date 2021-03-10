
import asyncio
import random
import time
import logging


format = '[%(asctime)s] %(levelname)s: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format=format)


async def part1(n: int) -> str:
    i = random.randint(0, 10)
    logger.debug(f"part1({n}) sleeping for {i} seconds.")
    await asyncio.sleep(i)
    result = f"result{n}-1"
    logger.info(f"Returning part1({n}) == {result}.")
    return result


async def part2(n: int, arg: str) -> str:
    i = random.randint(0, 10)
    logger.debug(f"part2{n, arg} sleeping for {i} seconds.")
    await asyncio.sleep(i)
    result = f"result{n}-2 derived from {arg}"
    logger.info(f"Returning part2{n, arg} == {result}.")
    return result


async def chain(n: int) -> None:
    start = time.perf_counter()
    p1 = await part1(n)
    p2 = await part2(n, p1)
    end = time.perf_counter() - start
    logger.info(f"-->Chained result{n} => {p2} (took {end:0.2f} seconds).")


async def main(*args):
    logger.info('Calling chain')
    await asyncio.gather(*(chain(n) for n in args))


if __name__ == "__main__":
    import sys
    random.seed(444)
    args = [1, 2, 3] if len(sys.argv) == 1 else map(int, sys.argv[1:])
    start = time.perf_counter()
    asyncio.run(main(*args))
    end = time.perf_counter() - start
    logger.debug(f"Program finished in {end:0.2f} seconds.")


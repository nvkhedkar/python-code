import asyncio
import random
import time, logging

format = '[%(asctime)s] %(levelname)s: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format=format)


async def heavy_work(n: int):
    i = 2 # random.randint(0, 2)
    logger.info(f"sleep for {i}")
    await asyncio.sleep(i)
    return f"finished {n}"


async def main(*args):
    results = await asyncio.gather(*(heavy_work(n) for n in args))
    logger.info(results)


if __name__ == "__main__":
    args = [1, 2, 3]

    start = time.perf_counter()
    asyncio.run(main(*args))

    end = time.perf_counter() - start
    logger.debug(f"Program finished in {end:0.2f} seconds.")

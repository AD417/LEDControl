import asyncio
from aio_stdout import ainput, aprint

delta = 1

async def countdown(n: int) -> None:
    """Count down from `n`, taking `n` seconds to run."""
    global delta
    i = 0
    while i < 1000000:
        i += delta
        await aprint(i)
        await asyncio.sleep(1)

async def get_name() -> str:
    """Ask the user for their name."""
    global delta
    while delta > 0:
        delta = int(await ainput("New delta: "))

async def main() -> None:
    await asyncio.gather(countdown(15), get_name())

if __name__ == "__main__":
    asyncio.run(main())


from aio_stdout import ainput, aprint
import asyncio
import time

class Timer:
    last = 0
    next = 1
    interval = 0.33333

    frames = 0

    running = True

    def set_next():
        Timer.last = Timer.next
        Timer.next = Timer.last + Timer.interval
        Timer.frames += 1


async def count():
    Timer.next = time.time() + 5
    while Timer.running: 
        if time.time() < Timer.next: continue
        Timer.set_next()
        # Ignore the fact that this is not aprint; ainput blocks aprint.
        print(Timer.frames)

async def get_input():
    # This absolutely does not run cleanly with the above. But I want 2 event loops, so...  
    while Timer.running:
        command = await ainput()
        if command == "exit":
            Timer.running = False
        else:
            await aprint(f"Input was {command}")

async def main():
    await asyncio.gather(get_input(), count())

if __name__ == '__main__':
    asyncio.run(main())
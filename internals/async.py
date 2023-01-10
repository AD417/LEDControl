import asyncio
import aioconsole

async def say_hi(message):
    for i in range(3):
        await asyncio.sleep(1)
        print(message)

async def test():
    _, response = await asyncio.gather(
        say_hi("world"),
        aioconsole.ainput('Is this your line? '),
    )
    print("response was", response)

for i in range(10):
    asyncio.run(test())
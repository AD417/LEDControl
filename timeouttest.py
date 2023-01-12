from aio_stdout import ainput, aprint
import concurrent.futures
import asyncio

class Timer:
    running = True
    interval = 1
    frames_left = 100

def perform_operations(): ...

async def get_input(event): 
    while Timer.running:
        # For this demo, we only care about numbers, not commands.
        command = await ainput()
        if command == "exit":
            Timer.running = False
            # Immediately tick the countdown. 
            event.set()
        else:
            try: 
                Timer.interval = float(command)
                event.set()
            except: await aprint(f"Invalid time: {command}")

async def countdown(event):
    while Timer.frames_left >= 0 and Timer.running:
        try: 
            await asyncio.wait_for(event.wait(), Timer.interval)
            event.clear()
            # Eventually, other logic will be inserted here. 
            perform_operations()
        except concurrent.futures.TimeoutError: pass
        except asyncio.TimeoutError: pass
        finally: 
            # This is for demonstration; It's pretty hideous.
            print(Timer.frames_left)
            Timer.frames_left -= 1
    
    Timer.running = False

async def main():
    # This event syncs both sides of this operation. 
    # I probably should create a new "countdown" task from the get_input function. 
    event = asyncio.Event()
    await asyncio.gather(countdown(event), get_input(event))

if __name__ == "__main__":
    asyncio.run(main()) 
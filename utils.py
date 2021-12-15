import asyncio

async def simulate_delay(seconds: float = 1):
    """Simulate server delay for specified seconds.

    Args:
        seconds (float, optional): Time in seconds. Defaults to 1.
    """    
    await asyncio.sleep(seconds)

def clear_line():
    """Removes current line in the console.
    """    
    print("\033[2K\033[1G", flush=True, end="")

async def animate_typing():
    """Animate loading using 3 dots.
    """    
    for _ in range (0,3):  
        await simulate_delay(0.3)
        print('.', end="", flush=True)
    await simulate_delay(0.3)
    clear_line()

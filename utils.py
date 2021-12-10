import time

def simulate_delay(seconds):
    time.sleep(seconds)

def clear_line():
    print("\033[2K\033[1G", flush=True, end="")

def animate_typing():
    for _ in range (0,3):  
        simulate_delay(0.3)
        print('.', end="", flush=True)
    simulate_delay(0.3)
    clear_line()

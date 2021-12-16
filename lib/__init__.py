import re
import time

def simulate_delay(seconds: float = 1):
    """Simulate server delay for specified seconds.

    Args:
        seconds (float, optional): Time in seconds. Defaults to 1.
    """    
    time.sleep(seconds)

def valid_email(email: str) -> bool:   
    return re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)
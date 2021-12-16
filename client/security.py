from lib import valid_email
import net
from collections.abc import Callable

def authenticate(MAX_ATTEMPTS: int) -> tuple:
    name = challenge("Name", MAX_ATTEMPTS, len)
    if not name:
        return (None, None, False)
    
    email = challenge("Email", MAX_ATTEMPTS, valid_email)
    if not email:
        return (None, None, False)

    send_token(email)

    print(f"A Token has been sent to {email}.")

    valid = challenge("Token", MAX_ATTEMPTS, valid_token)
    if not valid:
        return (None, None, False)
    
    return (name, email, True)

def challenge(type: str, MAX_ATTEMPTS: int, callback: Callable[[str], bool]):
    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        value = input(f"{type}: ")
        if callback(value):
            return value
        else:
            attempt += 1
            print(f"{MAX_ATTEMPTS - attempt + 1} attempt(s) left")
    return None

def valid_token(token: str) -> bool:
    net.write(net.current_socket, token)
    return bool(int(net.read(net.current_socket)))

def send_token(email: str):
    net.write(net.current_socket, email)

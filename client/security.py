'''
Provide client side security functions.
'''
from lib import valid_email
import net
from collections.abc import Callable

def authenticate(MAX_ATTEMPTS: int = 3) -> tuple:
    """Authenticate user before starting the chat by providing name, email, and
    a token sent to the email.

    Args:
        MAX_ATTEMPTS (int): Max number of failed attempts. Defaults to 3.

    Returns:
        tuple: Name, Email provided by user and whether the user is OK to 
        start chatting
    """    
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

def challenge(type: str,  callback: Callable[[str], bool], MAX_ATTEMPTS: int = 3) -> tuple:
    """Challenge the user to provide a correct value.

    Args:
        type (str): type of the challenge.
        callback (Callable[[str], bool]): Callback to test user input.
        MAX_ATTEMPTS (int): Max number of failed attempts. Defaults to 3.

    Returns:
        tuple: Last input value and the status of the challenge.
    """    
    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        value = input(f"{type}: ")
        if callback(value):
            return (value, True) 
        else:
            attempt += 1
            print(f"{MAX_ATTEMPTS - attempt + 1} attempt(s) left")
    return (value, False)

def valid_token(token: str) -> bool:
    """Check whether the token provided by the user is valid or not by 
    comparing it to the one on the server.

    Args:
        token (str): Token provided by user.

    Returns:
        bool: Whether the token is valid or not.
    """    
    net.write(net.current_socket, token)
    return bool(int(net.read(net.current_socket)))

def send_token(email: str):
    net.write(net.current_socket, email)

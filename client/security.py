'''
Provide client side security functions.
'''
import net
from collections.abc import Callable
import re

def valid_email(email: str) -> bool:   
    return re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)

def authenticate(MAX_ATTEMPTS: int = 3) -> tuple:
    """Authenticate user before starting the chat by providing name, email, and
    a token sent to the email.

    Args:
        MAX_ATTEMPTS (int): Max number of failed attempts. Defaults to 3.

    Returns:
        tuple: Name, Email provided by user and whether the user is OK to 
        start chatting
    """    
    name, OK = challenge("Name", len, MAX_ATTEMPTS)
    if not OK:
        return (None, None, False)
    
    email, OK = challenge("Email", valid_email, MAX_ATTEMPTS)
    if not OK:
        return (None, None, False)

    request_token(email)

    print(f"A Token has been sent to {email}.")

    _, OK = challenge("Token", valid_token, MAX_ATTEMPTS)
    if not OK:
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
    if len(token) == 0:
        return False
    net.write(net.current_socket, token)
    return bool(int(net.read(net.current_socket)))

def request_token(email: str):
    """Requset the server for a token

    Args:
        email (str): Email to send the token to.
    """    
    net.write(net.current_socket, email)

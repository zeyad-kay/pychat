'''
Implement server security functions.
Functions include email validation before starting the chat. A token is sent to
the user's provided email and the token must match the one on the server.
'''
import socket
import net

def valid_email(email: str) -> bool:   
    import re
    return re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)

def generate_token(email: str):
    """Generate a token and save it to Mongo

    Args:
        email (str): Email to bind the token to.

    Raises:
        ValueError: When the email is invalid.

    Returns:
        str: Generated Token.
    """    
    import secrets
    import mongo

    if not valid_email(email):
        raise ValueError("Invalid email.")
    
    mongo.db["tokens"].delete_one({
        "email": email
    })
    token = secrets.token_hex(20)
    mongo.db["tokens"].insert_one({
        "email": email,
        "token": token,
    })
    return token

def verify_token(email: str, token: str) -> bool:
    """Compare provided token with the one in the database binded by the email.

    Args:
        email (str): Email which the token is bind to.
        token (str): Token provided by user.

    Raises:
        ValueError: When the email is invalid.

    Returns:
        bool: Whether token is valid or not.
    """    
    import mongo
    
    if not valid_email(email):
        raise ValueError("Invalid email.")

    result = mongo.db["tokens"].find_one({"email": email})
    if not result:
        return False
    
    if result.get("token") == token:
        return True
    else:
        return False

def email_token(email: str, token: str):
    """Send token to user's email.

    Args:
        email (str): Email to send the token to.
        token (str): Token to send.
    
    Raises:
        ValueError: When the email is invalid or token is empty.
    """  
    import mail
    import os

    if not valid_email(email):
        raise ValueError("Invalid email.")
    if len(token) == 0:
        raise ValueError("Token is empty.")
    
    msg = f'''
    FROM: {os.environ.get("SENDER_EMAIL")}
    TO: {email}
    SUBJECT: Security Token

    Token: {token}
    '''
    mail.server.sendmail(from_addr=os.environ.get("SENDER_EMAIL"), to_addrs=email, msg=msg)

def authenticate(socket: socket.socket, MAX_ATTEMPTS: int) -> bool:
    """Authenticate user before starting the chat by sending a token to his email and 
    comparing that token to the entered one. It waits until authentication is done.

    Args:
        socket (socket) : socket between the client and the server.
        MAX_ATTEMPTS (int): maximum number of wrong tokens.

    Returns:
        bool: Whether user is authenticated or not.
    """    
    import mongo
    
    email = net.read(socket)
    
    generated_token = generate_token(email)
    # send mail
    email_token(email,generated_token)
    # second verify the token given by the client
    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        token = net.read(socket)
        if(verify_token(email,token)):
            net.write(socket,"1")
            mongo.db["tokens"].delete_one({ "email": email })
            return True
        else:
            attempt += 1
            net.write(socket,"0")

    mongo.db["tokens"].delete_one({ "email": email })
    return False
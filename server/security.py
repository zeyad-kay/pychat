'''
Implement server security functions.
Functions include email validation before starting the chat. A token is sent to
the user's provided email and the token must match the one on the server.
'''

def generate_token(email: str):
    """Generates a token and saves it to Mongo

    Args:
        email (str): Email to bind the token to.

    Raises:
        ValueError: When the email is invalid.

    Returns:
        str: Generated Token.
    """    
    import secrets
    from lib import valid_email
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
    from lib import valid_email
    import mongo
    
    if not valid_email(email):
        raise ValueError("Invalid email.")

    result = mongo.db["tokens"].find_one({"email": email})
    if not result:
        return False
    return result.get("token") == token

def email_token(email: str, token: str):
    """Send token to user's email.

    Args:
        email (str): Email to send the token to.
        token (str): Token to send.
    
    Raises:
        ValueError: When the email is invalid or token is empty.
    """  
    import mail
    from lib import valid_email
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

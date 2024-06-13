import hashlib
import os
import base64


def hash_password(password: str, salt: bytes = None) -> str:
    if not salt:
        salt = "Accuknox".encode('utf-8')

    salt = base64.b64encode(salt).decode('utf-8')
    key = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    return f"{salt}${key}"


def verify_password(stored_password: str, provided_password: str) -> bool:
    user_password = hash_password(provided_password)

    return user_password == stored_password
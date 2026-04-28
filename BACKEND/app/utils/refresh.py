import secrets
import hashlib


def create_opaque_token():
    return secrets.token_hex(64)


def token_hash(token: str):
    return hashlib.sha256(token.encode()).hexdigest()

import hashlib
import os
import binascii
from datetime import datetime, timedelta
import uuid


def generate_salt():
    # возвращаем hex, но при хешировании преобразуем назад в bytes
    return binascii.hexlify(os.urandom(16)).decode()


def hash_password(salt: str, password: str) -> str:
    salt_bytes = binascii.unhexlify(salt)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt_bytes, 100_000)
    return binascii.hexlify(dk).decode()


def generate_token():
    return uuid.uuid4().hex


def token_expiry(days=7):
    return datetime.utcnow() + timedelta(days=days)

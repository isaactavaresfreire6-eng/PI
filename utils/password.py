import hashlib
import os


def hash_password(password):
    # Gera um salt aleatório e retorna a senha no formato "salt$hash"
    salt = os.urandom(16).hex()
    hashed = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 260000
    ).hex()
    return f"{salt}${hashed}"


def verify_password(password, stored):
    # Compara a senha digitada com o hash armazenado
    try:
        salt, hashed = stored.split("$", 1)
        check = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), 260000
        ).hex()
        return check == hashed
    except ValueError:
        return False

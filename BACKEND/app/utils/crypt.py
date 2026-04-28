from pwdlib import PasswordHash

# Atualmente usa o Argon2 como hash recomendado/instalado
password_hasher = PasswordHash.recommended()


def verifify_password(password, hashed_password):
    return password_hasher.verify(password, hashed_password)


def get_password_hash(password):
    return password_hasher.hash(password)

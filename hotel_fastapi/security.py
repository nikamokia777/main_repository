from pwd import PasswordHash
password_hasher = PasswordHash.recomended()
def hash_password(password: str) -> str:
    return password_hasher.hash(password)
def verify_password(password: str, hashed_password: str) -> bool:
    return password_hasher.verify(password, hashed_password)
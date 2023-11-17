from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str):
    return bcrypt_context.hash(password)


def verify(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

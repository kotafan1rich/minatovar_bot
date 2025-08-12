from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash(string: str) -> str:
    return pwd_context.hash(string)


def verify_password(password: str, hashed_password) -> bool:
    return pwd_context.verify(password, hashed_password)

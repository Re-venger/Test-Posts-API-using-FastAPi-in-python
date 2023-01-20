from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def hashPass(password: str):
    return pwd_context.hash(password)


def verifyPass(attempt_password, hashed_pass):
    return pwd_context.verify(attempt_password, hashed_pass)
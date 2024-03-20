from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

def hashed_password(password:str):
    return pwd_context.hash(password)

def verify(password:str, hashedPassword:str):
    return pwd_context.verify(password, hashedPassword)
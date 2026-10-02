from datetime import timedelta,timezone,datetime
from pwdlib import PasswordHash
from jose import jwt
from app.config import setting
password_hash = PasswordHash.recommended()

SECRET_KEY = setting.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hashed_password(password: str)-> str:
    return password_hash.hash(password)

def verify_paswword(plain_password: str,hashed_password: str)-> bool:
    return password_hash.verify(plain_password,hashed_password)

def verify_pin(plain_pin:str, hashed_pin:str)-> bool:
    return password_hash.verify(str(plain_pin),hashed_pin)

def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire
    }

    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token
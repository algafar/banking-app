from fastapi.security import OAuth2PasswordBearer
from Oauth2.security import SECRET_KEY,ALGORITHM
from fastapi import Depends,HTTPException,status
from app.database import get_db
from sqlalchemy.orm import Session
from jose import jwt ,JWTError
from crud import Manager



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Login")
manager = Manager()

def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    users = manager.get_users_by_id(int(user_id),db)
    if users is None:
        raise credential_exception
    return users



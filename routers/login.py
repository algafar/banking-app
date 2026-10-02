from fastapi import APIRouter, Depends,HTTPException,status
from app.schemas import LoginRequest, Token
from sqlalchemy.orm import Session
from app.database import get_db
from Oauth2.security import create_access_token,verify_paswword
from crud import Manager
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/login", tags=["Login"])
manager = Manager()

@router.post('/',response_model=Token)
def Login(login_data:OAuth2PasswordRequestForm= Depends(),db:Session = Depends(get_db)):
    user = manager.get_users_by_email(login_data.username,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invalid email or password"
        )
    password_verification = verify_paswword(login_data.password,user.password_hash)

    if not password_verification:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid email or password"
        )

    token = create_access_token(user_id=user.user_id,role=user.role.value)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
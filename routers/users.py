from fastapi import APIRouter,status,HTTPException,Depends
from app.schemas import usersCreate,usersLoginResponse
from sqlalchemy.orm import Session
from app.database import get_db
from crud import Manager
from model import Users
from Oauth2.security import hashed_password


router = APIRouter(prefix="/signup", tags=["Signup"])
manager = Manager()

@router.post('/',response_model=usersLoginResponse,status_code=status.HTTP_201_CREATED)
def add_users(new_user:usersCreate,db:Session = Depends(get_db)):
    account_info = manager.get_account_info_by_email(new_user.email,db)
    


    existing_users= manager.get_users_by_email(new_user.email,db)
    
    try:
        if not account_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="email not found"
            )
        if existing_users:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail= "user already exists"
            )
        
        hash_password = hashed_password(new_user.password) 
        
    
        user = Users(email = account_info.email,password_hash = hash_password,role = account_info.role)
        db.add(user)
        db.commit()
        db.refresh(user)
        update_account = manager.update_user(user.user_id,db)
        return update_account
        
    
    except Exception as e:
        db.rollback()
        raise e
from role.role import Role
from fastapi import Depends,HTTPException,status
from Oauth2.dependencies import get_current_user
from model import Users

def require_admin(current_user: Users  = Depends(get_current_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current_user

def require_customer(current_user: Users = Depends(get_current_user)):
    if current_user.role != Role.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Customer access required"
        )
    return current_user        
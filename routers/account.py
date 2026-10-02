from app.schemas import NotificationResponse
from sqlalchemy.orm import Session
from app.database import get_db
from Oauth2.authorization import require_customer
from crud import Manager
from model import Users
from fastapi import Depends
from fastapi import APIRouter, status


router = APIRouter(prefix="/dashboard", tags=["Account"])
manager = Manager()

@router.get('/accounts',status_code=status.HTTP_200_OK)
def get_list_account(db:Session = Depends(get_db),current_user: Users = Depends(require_customer)):
    rows = manager.get_account_by_user_id(current_user.user_id,db)
    return [
        {
            "account_id": row.account_id,
            "account_number": row.account_number,
            "account_type": row.account_type,
            "balance": float(row.balance)
        }
        for row in rows
    ]
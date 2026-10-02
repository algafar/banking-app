from fastapi import APIRouter, Depends,HTTPException,status
from app.schemas import TransactionCreate,TransactionResponse
from model import Users,Transactions
from sqlalchemy.orm import Session
from app.database import get_db
from crud import Manager
from Oauth2.authorization import require_customer


router = APIRouter(prefix="/dashboard", tags=["dashboard"])
manager = Manager()

@router.get('/',status_code=status.HTTP_200_OK)
def get_dashboard(db:Session = Depends(get_db),current_user: Users = Depends(require_customer)):
    user_info = manager.get_account_info_by_email(current_user.email,db)
    user_accounts = manager.get_account_by_user_id(current_user.user_id,db)


    return {
        "id": current_user.user_id,
        "user_id": current_user.user_id,
        "users": {
            "first_name":user_info.first_name,
            "last_name": user_info.last_name,
            "email": user_info.email,
            "country": user_info.country,
            "city": user_info.city,
            "address": user_info.address,
            "profile_picture":current_user.profile_picture
        },
        "account": [
            {
                "account_type": acc.account_type,
                "account_number": acc.account_number,
                "balance": acc.balance
            }
            for acc in user_accounts
        ],
    }
    
       
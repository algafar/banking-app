from app.schemas import TransactionResponse
from sqlalchemy.orm import Session
from app.database import get_db
from Oauth2.authorization import require_customer
from crud import Manager
from model import Users
from fastapi import Depends,HTTPException
from fastapi import APIRouter, status
from typing import List


router = APIRouter(prefix="/dashboard", tags=["Transactions"])
manager = Manager()

@router.get('/transactions',response_model=List[TransactionResponse],status_code=status.HTTP_200_OK)
def get_user_transaction(db:Session = Depends(get_db),current_user: Users = Depends(require_customer)):
    transactions = manager.get_user_transac(current_user.user_id,db)
    return transactions
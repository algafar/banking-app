from fastapi import APIRouter, Depends,HTTPException,status
from app.schemas import TransactionCreate,TransactionResponse
from model import Users,Transactions
from sqlalchemy.orm import Session
from app.database import get_db
from crud import Manager
from Oauth2.authorization import require_customer
from Oauth2.security import verify_pin

router = APIRouter(prefix="/dashboard", tags=["Local_transfer"])
manager = Manager()

@router.post('/transfer/internal', response_model=TransactionResponse,status_code=status.HTTP_200_OK)
def wiretransfer(transfer_in:TransactionCreate,db:Session = Depends(get_db),current_user: Users = Depends(require_customer)):
    
    user_account = manager.get_account_info_by_email(current_user.email,db)
    source_account = manager.get_account_by_source_type(user_account.account_number,transfer_in.from_a,db)
    if not source_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    if source_account.balance < transfer_in.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds"
        )
    pin_correct = verify_pin(transfer_in.transaction_pin_hash,current_user.transaction_pin_hash)
    if not pin_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect pin"
        )
    try:
        source_account.balance -= transfer_in.amount
        transfer = Transactions(
            from_a = transfer_in.from_a,
            type = "INTERNAL_TRANSFER",
            beneficiary_account = transfer_in.beneficiary_account,
            amount = transfer_in.amount,
            beneficiary_name = transfer_in.beneficiary_name,
            remark = transfer_in.remark,
            pin = current_user.transaction_pin_hash
        )
        db.add(transfer)
        db.commit()
        db.refresh(transfer)
        return transfer
    except Exception as e:
        db.rollback()
        print("TRANSACTION ERROR DETAILS:", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"transaction failed:{str(e)}"
        )


    
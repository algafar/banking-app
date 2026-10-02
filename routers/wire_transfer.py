from fastapi import APIRouter, Depends,HTTPException,status,Request
from app.schemas import TransactionCreate,TransactionResponse
from model import Users,Transactions
from sqlalchemy.orm import Session
from app.database import get_db
from crud import Manager
from Oauth2.authorization import require_customer
from Oauth2.security import verify_paswword
from datetime import datetime
from zoneinfo import ZoneInfo

router = APIRouter(prefix="/dashboard", tags=["Wire_transfer"])
manager = Manager()

@router.post('/transfer/wire',response_model=TransactionResponse,status_code=status.HTTP_201_CREATED)
async def wiretransfer(request: Request, transfer_in: TransactionCreate, db:Session = Depends(get_db),current_user: Users = Depends(require_customer)):
    us_eastern_now = datetime.now(ZoneInfo("America/New_York"))
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
    pin_correct = verify_paswword(transfer_in.pin,current_user.transaction_pin_hash)
    if not pin_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect pin"
        )
    if source_account.status and source_account.status.upper() == "FROZEN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail=f"Transaction declined: Your accout has been tmporarily restricted due to security review. Kindly contact customer support review for further assistance"
        )
    try:
        source_account.balance -= transfer_in.amount
        transfer = Transactions(
            from_a = transfer_in.from_a,
            user_id= current_user.user_id,
            type = "WIRE_TRANSFER",
            bank_name = transfer_in.bank_name,
            routing_number = transfer_in.routing_number,
            swift_code = transfer_in.swift_code,
            beneficiary_account = transfer_in.beneficiary_account,
            beneficiary_name = transfer_in.beneficiary_name,
            amount = transfer_in.amount,
            remark = transfer_in.remark,
            pin = current_user.transaction_pin_hash,
            fee = 100.0,
            date = us_eastern_now
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


    
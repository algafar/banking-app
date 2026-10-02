from fastapi import APIRouter,Depends,HTTPException,status
from app.schemas import AccountRegCreate,AccountRegResponse,AccountCreate,AccountBalanceResponse
from sqlalchemy.orm import Session
from app.database import get_db
from crud import Manager
from model import AccoountReg,Account



router = APIRouter(prefix="/register", tags=["AccountRegistration"])
manager = Manager()

account_number = manager.generate_account_number()
@router.post('/',response_model=AccountRegResponse, status_code=status.HTTP_201_CREATED)
def add_account(new_account: AccountRegCreate,db:Session = Depends(get_db)):

    saving_account_number = manager.generate_account_number() 
    checking_account_number = manager.generate_account_number()
    first_name = new_account.first_name
    last_name = new_account.last_name
    gender = new_account.gender
    dob = new_account.dob
    address = new_account.address
    email = new_account.email
    country = new_account.country
    city = new_account.city
    initial_balance = new_account.initial_balance
    #Accounreg instance
    existing_account = manager.get_account_info_by_email(email,db)
    try:
        if existing_account:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail= "email already exist"
            )
        accountreg_in = AccoountReg(
            account_number = saving_account_number,
            first_name = first_name,
            last_name = last_name,
            gender = gender,
            dob = dob,
            address = address,
            email = email,
            country = country,
            city = city,
            initial_balance = initial_balance,
            role = "customer"
        )
        db.add(accountreg_in)
        savings_account = Account(
            account_number = accountreg_in.account_number,
            account_type = "saving",
            balance = accountreg_in.initial_balance
        )
        db.add(savings_account)
        checking_account = Account(
            account_number = checking_account_number,
            account_type = "checking",
            balance = 350.0
        )
        db.add(checking_account)
        db.commit()
        return accountreg_in
    except Exception as e:
        db.rollback()
        raise e
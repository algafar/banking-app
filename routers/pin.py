from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from Oauth2.authorization import require_customer
from app.database import get_db
from sqlalchemy.orm import Session
from model import Users
from crud import Manager
from Oauth2.security import hashed_password



class PinCreateSchema(BaseModel):
    pin: str
router = APIRouter(prefix="/dashboard")
manager = Manager()

@router.post("/settings/pin")
def set_user_pin(payload: PinCreateSchema, current_user: Users = Depends(require_customer), db:Session = Depends(get_db)):
    # Validate PIN length or format if needed
    if len(payload.pin) != 4 or not payload.pin.isdigit():
        raise HTTPException(status_code=400, detail="PIN must be 4 digits")

    hash_pass = hashed_password(payload.pin)
    
    manager.update_pin(current_user.user_id,hash_pass,db)
    
    return {"message": "PIN saved successfully"}
from pydantic import BaseModel,ConfigDict, EmailStr,Field
from datetime import datetime,date
from decimal import Decimal



class AccountRegCreate(BaseModel):
    first_name: str
    last_name: str
    gender: str
    dob: date
    address: str
    email: EmailStr
    country: str
    city: str
    initial_balance: Decimal

class AccountRegResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    reg_id: int
    account_number: str
    first_name: str
    last_name: str
    dob: date
    address: str
    email: EmailStr
    country: str
    city: str
    initial_balance: Decimal
    date: datetime

class AccountCreate(BaseModel):
    account_number: str
    account_type: str
    balance: Decimal

class AccountBalanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    account_id: int
    account_number: str
    account_type: str
    balance: Decimal
    
class usersCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class usersLoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    email: EmailStr
    role: str
    profile_picture: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class LocalTransferCreate(BaseModel):
    from_a: str
    bank_name: str
    routing_number: str
    beneficiary_account: str
    beneficiary_name: str
    amount: Decimal
    remark: str
    transaction_pin_hash: str

class LocalTransferResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transaction_id: str
    from_a: str
    bank_name: str
    routing_number: str
    beneficiary_account: str
    beneficiary_name: str
    amount: Decimal
    remark: str
    

class WireTransferCreate(BaseModel):
    from_a: str
    bank_name: str
    routing_number: str
    swift_code: str
    beneficiary_account: str
    beneficiary_name: str
    amount: Decimal
    remark: str
    transaction_pin_hash: str

class WireTransferResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transaction_id: str
    from_a: str
    bank_name: str
    routing_number: str
    swift_code: str
    beneficiary_account: str
    beneficiary_name: str
    amount: Decimal
    remark: str
    

class TransactionCreate(BaseModel):
    from_a: int
    bank_name: str
    routing_number: str
    swift_code: str
    beneficiary_account: str
    beneficiary_name: str
    amount: Decimal
    remark: str
    pin: str


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transaction_id: int
    from_a: int
    reference_id: str
    bank_name: str
    routing_number: str
    swift_code: str
    beneficiary_account: str
    beneficiary_name: str
    amount: Decimal
    remark: str
    fee: Decimal
    date: datetime
    status: str

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message:str
    type: str

class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    title: str
    message: str
    type: str
    read: bool
    created_at: datetime


class AdminReplyCreate(BaseModel):
    room_id: int
    message: str
    sender_type: str = "ADMIN"
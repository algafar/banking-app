from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,String,ForeignKey,Text,Boolean
from sqlalchemy import DateTime,Date,func
from app.database import Base
from sqlalchemy import Enum,UniqueConstraint,Numeric,CheckConstraint
from role.role import Gender,Role,AccountType,TransferType,ChatStatus,Status,AccountStatus
from sqlalchemy import Enum 
from datetime import date,datetime
from zoneinfo import ZoneInfo
from typing import Optional
import uuid


class AccoountReg(Base):
    __tablename__ = "accountreg"
    
    reg_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_number: Mapped[str] = mapped_column(String(20),nullable=False,)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(Gender, native_enum=False))
    dob: Mapped[date] = mapped_column(Date, nullable=False)
    address: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    initial_balance: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role, native_enum=False,default=Role.CUSTOMER)) 
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("America/New_York")))
   


    __table_args__ = (
        UniqueConstraint("email", name="uq_accountref_email"),
        UniqueConstraint("account_number", name="uq_accountref_account_number")
                
    )

class Account(Base):
    __tablename__ = "account"

    account_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_number: Mapped[str] = mapped_column(String(50), nullable=False)
    account_type: Mapped[AccountType] = mapped_column(Enum(AccountType, native_enum=False))
    balance: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=True)
    status: Mapped[AccountStatus] = mapped_column(Enum(AccountStatus, native_enum=False), default=AccountStatus.ACTIVE, nullable=False)

    users: Mapped["Users"] = relationship(
        back_populates="account"
    )
    __table_args__ = (
        CheckConstraint('balance >=0',name='non_negative_balance'),
    )
class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    transaction_pin_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[Role] = mapped_column(Enum(Role, native_enum=False),nullable=False)
    profile_picture: Mapped[str] = mapped_column(String(255), nullable=True)

    account: Mapped[list["Account"]] = relationship(
        back_populates="users"
    )
    chat_rooms: Mapped["Chatroom"] = relationship(
        back_populates="users"
    )
    chat_messages: Mapped[list["Chatmessage"]] = relationship(
        back_populates="users", foreign_keys="[Chatmessage.sender_id]"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="users"
    )
    transactions: Mapped[list["Transactions"]] = relationship(
        back_populates="users"
    )

class Transactions(Base):
    __tablename__ = "transaction_table"

    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    from_a: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[TransferType] = mapped_column(Enum(TransferType, native_enum=False), nullable=False)
    beneficiary_account: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    beneficiary_name: Mapped[str] = mapped_column(String(255), nullable=False)
    bank_name: Mapped[str] = mapped_column(String(255), nullable=False)
    swift_code: Mapped[str] = mapped_column(String(100), nullable=True)
    routing_number: Mapped[str] = mapped_column(String(100), nullable=False)
    remark: Mapped[str] = mapped_column(String(255), nullable=True)
    pin: Mapped[str] = mapped_column(String(255), nullable=False)
    bank_address: Mapped[str] = mapped_column(String(255), nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fee: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status, native_enum=False), default=Status.PENDING)
    reference_id: Mapped[str] = mapped_column(String(50),unique=True, nullable=False, default=lambda: f"REF-{uuid.uuid4().hex[:8].upper()}")

    users: Mapped["Users"] = relationship(
        back_populates="transactions"
    )

class Chatroom(Base):
    __tablename__ = "chat_rooms"
    room_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"))
    status: Mapped[ChatStatus] = mapped_column(Enum(ChatStatus, native_enum=False), default=ChatStatus.OPEN,nullable=False)
    created_at: Mapped[datetime]= mapped_column(DateTime(timezone=True),server_default=func.now())

    chat_messages: Mapped[list["Chatmessage"]] = relationship(
        back_populates="chat_rooms"
    )
    users: Mapped["Users"] = relationship(
        back_populates="chat_rooms", foreign_keys=[user_id]
    )

class Chatmessage(Base):
    __tablename__ = "chat_messages"
    chat_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_room_id: Mapped[int] = mapped_column(Integer,ForeignKey("chat_rooms.room_id"))
    sender_id: Mapped[str] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=True)
    recipient_id: Mapped[Optional[str]] = mapped_column(Integer,ForeignKey("users.user_id", ondelete="CASCADE"), nullable=True)
    sender_type: Mapped[Role]= mapped_column(Enum(Role, native_enum=False),nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    chat_rooms: Mapped["Chatroom"] = relationship(
        back_populates="chat_messages"
    )
    users: Mapped["Users"] = relationship(
        back_populates="chat_messages", foreign_keys=[sender_id]
    )

class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())

    users: Mapped["Users"] = relationship(
        back_populates="notifications"
    )
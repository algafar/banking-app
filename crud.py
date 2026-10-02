from model import Users,AccoountReg,Transactions,Account,Chatroom,ChatStatus,Notification
from app.schemas import AccountRegCreate,usersCreate,WireTransferCreate,WireTransferResponse
from sqlalchemy.orm import Session
from sqlalchemy import select,update
import random
from typing import List,Sequence
class Manager:
    def create_account(self,account: AccountRegCreate,session:Session):
        session.add(account)
        session.commit()
        session.refresh(account)
        return account

    def get_account_info_by_email(self,email,session:Session):
        return session.scalars(select(AccoountReg).where(AccoountReg.email == email)).first()

    def get_account_by_account_id(self,account_id,session:Session):
        return session.scalar(select(Account).where(Account.account_id == account_id))

    def get_account_by_account_number(self,account_number,session:Session):
        return session.scalar(select(Account).where(Account.account_number == account_number))

    def get_account_by_user_id(self,user_id,session:Session):
        return session.scalars(select(Account).where(Account.user_id==user_id)).all()

    def update_user(self,new_user_id,session:Session):
        stmt = (
            update(Account).where(Account.user_id==None).values(user_id=new_user_id)
        )
        session.execute(stmt)
        session.commit()

    def get_account_by_source_type(self,account_number,source_type,session:Session):
        stmt =(
            select(Account).where(Account.account_number == account_number,Account.account_id==source_type).with_for_update()
        )
        return session.scalar(stmt)


    def generate_account_number(self):
        return str(random.randint(1000000000, 9999999999))

    #user
    def add_users(self,user:usersCreate,session:Session):
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def get_users(self,session:Session):
        return session.scalars(select(Users)).all()

    def get_users_by_email(self,email,session:Session):
        return session.scalars(select(Users).where(Users.email== email)).first()

    def get_users_by_id(self,id:int,session:Session):
        return session.scalar(select(Users).where(Users.user_id==id))

    def update_pin(self,user_id:int, pin:str,session:Session):
        stmt = (
            update(Users).where(Users.user_id==user_id).values(transaction_pin_hash=pin)
        )
        session.execute(stmt)
        session.commit()
    #transactions
    def wire_transfer(self,transfer:WireTransferCreate,session:Session):
        session.add(transfer)
        session.commit()
        session.refresh(transfer)
        return transfer

    def get_or_create_room(self,user_id:int,session:Session):
        uid = int(user_id) if str(user_id).isdigit() else user_id
        stmt = select(Chatroom.room_id).where(Chatroom.user_id==uid,Chatroom.status=="OPEN")
        room_id = session.scalars(stmt).first()
        if not room_id:
            room = Chatroom(user_id=uid,status="OPEN")
            session.add(room)
            session.flush()
            room_id = room.room_id
        return room_id

    def get_recipient(self,room_id:int,session:Session):
        stmt = select(Chatroom).where(Chatroom.room_id==int(room_id))
        return session.scalars(stmt).first()
    #notification
    def get_notification(self,user_id:int,session:Session): 
        return session.scalar(select(Notification).where(Notification.user_id == user_id))

    def get_user_transac(self,user_id,session:Session):
        return session.scalars(select(Transactions).where(Transactions.user_id==user_id).order_by(Transactions.date.desc())).all()
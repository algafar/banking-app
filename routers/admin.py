from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Import your existing Auth / DB dependencies
from app.database import get_db
from model import Users,Account
from Oauth2.authorization import require_admin  
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from model import Chatroom,Chatmessage
from app.schemas import AdminReplyCreate
from pydantic import BaseModel
from crud import Manager
from role.role import ChatStatus

class StatusUpdate(BaseModel):
    status: str

router = APIRouter(prefix="/admin", tags=["ADMIN"])
manager = Manager()

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db

# 1. Get all users along with their account statuses
@router.get("/users")
def get_all_users(db: Session = Depends(get_db), current_admin: Users = Depends(require_admin)):
    users = manager.get_users(db)
    result = []
    for u in users:
        # Fetch the user's accounts to check their status
        accounts = manager.get_account_by_user_id(u.user_id,db)
        # Determine overall status (if any account is frozen, mark as frozen)
        primary_status = "ACTIVE"
        for acc in accounts:
            if acc.status == "FROZEN":
                primary_status = "FROZEN"
                break
                
        result.append({
            "user_id": u.user_id,
            "email": u.email,
            "status": primary_status
        }) 
    return result

# 2. Freeze all accounts associated with a user
@router.put("/users/{user_id}/freeze")
def freeze_user(user_id: int, db: Session = Depends(get_db), current_admin: Users = Depends(require_admin)):
    accounts = manager.get_account_by_user_id(user_id,db)
    if not accounts:
        raise HTTPException(status_code=404, detail="No accounts found for this user")
    
    for acc in accounts:
        acc.status = "FROZEN"
    db.commit()
    return {"message": "User accounts frozen successfully"}

# 3. Unfreeze all accounts associated with a user
@router.put("/users/{user_id}/unfreeze")
def unfreeze_user(user_id: int, db: Session = Depends(get_db), current_admin: Users = Depends(require_admin)):
    accounts = manager.get_account_by_user_id(user_id,db)
    if not accounts:
        raise HTTPException(status_code=404, detail="No accounts found for this user")
    
    for acc in accounts:
        acc.status = "ACTIVE"
    db.commit()
    return {"message": "User accounts unfrozen successfully"}

@router.get("/")
def verify_admin_session( current_user: Users = Depends(require_admin),db: Session = Depends(get_db)):
    
    # Optional: Check if user is actually an admin
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Not authorized as admin")
    
    return {
        "status": "authenticated",
        "user_id": current_user.user_id,
        "email": current_user.email
    }

@router.get("/support")
def verify_admin(current_user: Users = Depends(require_admin), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin required"
        )
    

    
    # Optional: Check if user is actually an admin
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Not authorized as admin")
    
    return {"status": "authorized", "message": "Admin session is valid"}


@router.get("/chat-rooms")
def get_admin_chat_rooms(current_user: Users = Depends(require_admin), db: Session = Depends(get_db)):
    stmt = select(Chatroom).options(
        selectinload(Chatroom.users),
        selectinload(Chatroom.chat_messages)
    ).order_by(Chatroom.created_at.desc())
    
    rooms = db.scalars(stmt).all()
    return rooms




@router.post("/support/reply")
def send_admin_reply(
    reply: AdminReplyCreate, 
    current_user: Users = Depends(require_admin), 
    db: Session = Depends(get_db)
):
    # Create the new chat message tied to the room
    new_message = Chatmessage(
        chat_room_id=reply.room_id,
        sender_id=str(current_user.user_id), # or current_user's identifier
        sender_type=reply.sender_type,
        message=reply.message
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return {"status": "success", "message": "Reply sent successfully", "data": new_message}



@router.patch("/support/rooms/{room_id}/status")
async def update_room_status(room_id: int, payload: StatusUpdate, db: Session = Depends(get_db)):
    """
    Updates the status (OPEN, IN_PROGRESS, RESOLVED) of a specific chat room in the database.
    """
    try:
        stmt = select(Chatroom).where(Chatroom.room_id == room_id)
        room = db.scalars(stmt).first()
        if not room:
            raise HTTPException(status_code=404, detail="Chat room not found")
        new_status_str = payload.status.strip().upper()
        try:
            room.status = ChatStatus[new_status_str]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid status value: {new_status_str}")
        db.commit()
        db.refresh(room)
        
        return {"success": True, "room_id": room_id, "status": payload.status.upper()}
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
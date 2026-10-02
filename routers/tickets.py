# app/routers/tickets.py
from app.database import get_db
from model import Chatmessage
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from crud import Manager
from connection_manager import ConnectionManager

# Import your database session, models, and WebSocket connection manager
# from ..database import get_db
# from ..models import Chatroom, Chatmessage
# from ..connection_manager import manager

router = APIRouter(prefix="/dashboard", tags=["Tickets"])
manager = Manager()
websocket_manager = ConnectionManager()

class TicketCreateRequest(BaseModel):
    user_id: int
    user_email: EmailStr
    subject: str
    message: str

@router.post("/support/tickets")
async def create_ticket(data: TicketCreateRequest, db: Session = Depends(get_db)):
    # 1. Fetch existing active chat room for this user or create a new one
    room_id = manager.get_or_create_room(data.user_id,db)
    
    # 2. Format the ticket submission
    formatted_message = (
        f"【Support Ticket Submission】\n"
        f"Email: {data.user_email}\n"
        f"Subject: {data.subject}\n\n"
        f"{data.message}"
    )
    
    # 3. Save to chat_messages (including recipient_id as None for broadcast support rooms)
    new_message = Chatmessage(
        chat_room_id=room_id,
        sender_id=str(data.user_id),
        recipient_id=None,  # Optional: Set to None for general support queue, or pass agent_id if assigned
        sender_type="CUSTOMER",
        message=formatted_message
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    # 4. Construct payload and broadcast live over WebSocket
    payload = {
        "event": "new_message",
        "room_id": room_id,
        "message_id": new_message.chat_id,
        "sender_id": str(data.user_id),
        "recipient_id": None,
        "sender_type": "CUSTOMER",
        "message": formatted_message,
        "created_at": new_message.created_at.isoformat() if new_message.created_at else None
    }
    
    await websocket_manager.broadcast_to_admins(payload)
    
    return {
        "status": "success",
        "message": "Ticket successfully submitted and delivered to live chat!",
        "data": {
            "room_id": room_id,
            "message_id": new_message.chat_id
        }
    }
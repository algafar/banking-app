from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from model import Chatmessage
from app.database import get_db
from connection_manager import manager
from crud import Manager
from role.role import Role

router = APIRouter(prefix="/ws/support/users", tags=["User support chat"])
crud_manager = Manager()


@router.get("/health", tags=["user support chat"])
async def check_user_chat_status():
    return {"status": "user chat router is active"}


@router.websocket("/{user_id}")
async def support_chat_websocket(
    websocket: WebSocket, user_id: str, token: str = None, db: Session = Depends(get_db)
):
    await manager.connect_user(user_id, websocket)

    room_id = crud_manager.get_or_create_room(user_id, db)

    try:
        while True:
            # Removed the inner try/except so disconnections bubble up properly to the outer WebSocketDisconnect block
            data = await websocket.receive_json()

            text = data.get("message")
            if not text:
                continue

            # Cast user_id string to integer for relational DB column
            user_id_int = int(user_id) if user_id.isdigit() else user_id

            db_message = Chatmessage(
                chat_room_id=room_id,
                sender_id=user_id_int,
                sender_type=Role.CUSTOMER,
                message=text,
            )
            db.add(db_message)
            db.commit()
            db.refresh(db_message)

            created_time = (
                db_message.created_at or datetime.now(timezone.utc)
            ).isoformat()

            outgoing_payload = {
                "chat_id": db_message.chat_id,
                "chat_room_id": room_id,
                "sender_id": user_id,
                "sender_type": Role.CUSTOMER.value,
                "message": text,
                "created_at": created_time,
            }

            await manager.broadcast_to_admins(outgoing_payload)
            await manager.send_personal_message(outgoing_payload, str(user_id))

    except WebSocketDisconnect:
        # Use await if disconnect_user is async, remove await if it's a standard def function
            await manager.disconnect_user(user_id)
            print(f"User {user_id} disconnected normally")
              
    except Exception as e:
        await manager.disconnect_user(user_id)
        if "Connection closed" not in str(e) and "1000" not in str(e):
            print(f"Websocket error for user {user_id}: {e}")
        try:
            await websocket.close()
        except RuntimeError:
            pass # Socket might already be closed

@router.get("/chat/history/{user_id}")
async def get_user_chat_history(user_id: str, db: Session = Depends(get_db)):
    # 1. Get or create the room for this user
    room_id = crud_manager.get_or_create_room(user_id, db)
    
    # 2. Query all messages for this room from the database
    messages = db.query(Chatmessage).filter(Chatmessage.chat_room_id == room_id).all()
    
    # 3. Format them into a clean JSON list for the frontend
    formatted_messages = [
        {
            "chat_id": msg.chat_id,
            "chat_room_id": room_id,
            "sender_id": str(msg.sender_id),
            "sender_type": msg.sender_type.value if hasattr(msg.sender_type, 'value') else msg.sender_type,
            "message": msg.message,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
        }
        for msg in messages
    ]
    
    return {"messages": formatted_messages}
from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from model import Chatmessage
from app.database import get_db
from connection_manager import manager
from crud import Manager
from role.role import Role

router = APIRouter(prefix="/ws/support/admin", tags=["Admin support chat"])
crud_manager = Manager()


@router.get("/health", tags=["admins support chat"])
async def check_admin_chat_status():
    return {"status": "admin chat router is active"}


@router.websocket("")
@router.websocket("/")
async def admin_support_chat_websocket(
    websocket: WebSocket, db: Session = Depends(get_db)
):
    await manager.connect_admin(websocket)

    try:
        while True:
            try:
                data = await websocket.receive_json()
            except Exception:
                # Handle malformed client payloads gracefully
                continue

            room_id = data.get("chat_room_id")
            text = data.get("message")

            if not text or not room_id:
                continue

            chat_room = crud_manager.get_recipient(room_id, db)

            if not chat_room:
                await websocket.send_json(
                    {
                        "error": "INVALID RECIPIENT",
                        "detail": f"CHAT ROOM {room_id} NOT FOUND",
                    }
                )
                continue

            recipient_id = chat_room.user_id

            # Save message (sender_id is None or 0 for Admin)
            db_message = Chatmessage(
                chat_room_id=int(room_id),
                sender_id=None,
                recipient_id=int(recipient_id),
                sender_type=Role.ADMIN,
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
                "sender_id": "SUPPORT AGENT",
                "recipient_id": recipient_id,
                "sender_type": Role.ADMIN.value,
                "message": text,
                "created_at": created_time,
            }

            await manager.broadcast_to_admins(outgoing_payload)
            await manager.send_personal_message(outgoing_payload, str(recipient_id))

    except WebSocketDisconnect:
        manager.disconnect_admin(websocket)
    except Exception as e:
        manager.disconnect_admin(websocket)
        await websocket.close()
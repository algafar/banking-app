from app.schemas import NotificationResponse
from sqlalchemy.orm import Session
from app.database import get_db
from Oauth2.authorization import require_customer
from crud import Manager
from model import Users
from fastapi import Depends,HTTPException
from fastapi import APIRouter, status


router = APIRouter(prefix="/notifications", tags=["Notification"])
manager = Manager()

@router.get('/',response_model=NotificationResponse,status_code=status.HTTP_200_OK)
def get_notification(db:Session = Depends(get_db),current_user: Users = Depends(require_customer)):
    try:
        user_notification = manager.get_notification(current_user.user_id,db)
        if not user_notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found"
            )
        
        return user_notification
    except Exception as he:
        raise he
    except Exception as e:
        print(f"Error fetching notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))
 
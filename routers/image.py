import shutil
import os
import traceback
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from Oauth2.authorization import get_current_user
from model import Users
from app.database import get_db

router = APIRouter(prefix='/profile', tags=["Profile"])

# Directory where uploaded images will be saved locally
UPLOAD_DIR = "static/profiles"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-picture/")
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: Users = Depends(get_current_user), # Your existing auth dependency
    db: Session = Depends(get_db) # Your database session dependency
):
    try:
        # Create a unique filename using user ID to prevent collisions
        file_extension = file.filename.split(".")[-1]
        file_name = f"user_{current_user.user_id}_profile.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        # Save the uploaded file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Save the accessible URL path to the database
        image_url = f"http://localhost:8001/static/profiles/{file_name}"
        current_user.profile_picture = image_url
        db.commit()
        db.refresh(current_user)

        return {"message": "Profile picture updated successfully"}
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
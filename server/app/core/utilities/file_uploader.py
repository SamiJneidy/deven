import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from app.core.config.settings import settings

cloudinary.config( 
    cloud_name = settings.CLOUDINARY_CLOUD_NAME, 
    api_key = settings.CLOUDINARY_API_KEY, 
    api_secret = settings.CLOUDINARY_API_SECRET,
    secure=True
)

def upload_file(file: UploadFile, folder: str) -> tuple[str, str]:
    """Uploads a file to Cloudinary and returns the URL and public_id as tuple (secure_url, public_id)."""
    try:
        response = cloudinary.uploader.upload(file.file, folder=folder)
        return response["secure_url"], response["public_id"]
    except Exception as e:
        raise e
    
def delete_file(public_id: str) -> None:
    """Deletes a resource from Cloudinary using its public_id."""
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception as e:
        raise e
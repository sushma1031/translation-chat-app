import cloudinary
import cloudinary.uploader

import dotenv
import os
from pathlib import Path

CLOUD_DIR="trans-chat"

def upload_to_cld(path, type):
  dotenv.load_dotenv()

  # Configuration       
  cloudinary.config( 
    cloud_name = os.environ['CLOUD_NAME'], 
    api_key = os.environ['API_KEY'], 
    api_secret = os.environ['API_SECRET'],
    secure=True
  )
  resource = type if type == "image" else "video"
  filename = f"{CLOUD_DIR}/{type}/{Path(path).stem}"
  upload_result = cloudinary.uploader.upload(path, public_id=filename, resource_type=resource)
  return upload_result["secure_url"]
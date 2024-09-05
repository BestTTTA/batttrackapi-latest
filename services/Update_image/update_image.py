from fastapi import APIRouter, UploadFile, File, HTTPException
from minio import Minio
from minio.error import S3Error
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

router = APIRouter(tags=["Project => Upload Image"])

# Get environment variables
BUCKET_NAME = os.getenv("BUCKET_NAME")
DOMAIN = os.getenv("MINIO_DOMAIN")
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

# Initialize Minio client
minioClient = Minio(
    DOMAIN,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False  # Change to True if using HTTPS
)

try:
    if not minioClient.bucket_exists(BUCKET_NAME):
        minioClient.make_bucket(BUCKET_NAME)
    else:
        # Set the policy to allow public access to the bucket
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*",
                }
            ],
        }
        policy_json = json.dumps(policy)
        minioClient.set_bucket_policy(BUCKET_NAME, policy_json)
except S3Error as e:
    print(f"Error occurred: {e}")

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Use file size from FastAPI UploadFile
        file_size = await file.seek(0, os.SEEK_END)  # Get file size
        await file.seek(0)  # Reset file pointer to start

        minioClient.put_object(
            BUCKET_NAME,
            file.filename,
            file.file,
            file_size,
            content_type=file.content_type  # Set content type
        )
        
        return {
            "image_url": f"http://{DOMAIN}/{BUCKET_NAME}/{file.filename}"
        }
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {e}")

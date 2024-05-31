from fastapi import APIRouter, UploadFile, File
from minio import Minio
import os
import json

router = APIRouter(tags=["Project => Upload Image"])


BUCKET_NAME = "batttrack-bucket"
DOMAIN = "119.59.99.194:9000"

minioClient = Minio(
    DOMAIN,
    access_key="VPR0NDeYpA4LkklDrhal",
    secret_key="066PFXCDlVeZs9WBdRPrgYWC1Zn2hg7FkWeKtkXT",
    secure=False,
)



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

    # Set the bucket policy
    minioClient.set_bucket_policy(BUCKET_NAME, policy_json)


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_size = os.fstat(file.file.fileno()).st_size
    ret = minioClient.put_object(f"{BUCKET_NAME}", file.filename, file.file, file_size)
    return {
        "image_url": f"http://{DOMAIN}/{BUCKET_NAME}/" + ret._object_name
    }

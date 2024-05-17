from fastapi import APIRouter, UploadFile, File
from minio import Minio
import os
import json

router = APIRouter(tags=["Project => Upload Image"])


minioClient = Minio(
    "119.59.102.68:9000",
    access_key="9Ve1u4iU5FD9hzIK6eIZ",
    secret_key="havdRCufvaaKVPdIuQcGKSVLoIEGGYpp1E3APumG",
    secure=False,
)

BUCKET_NAME = "batttrack"

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
    ret = minioClient.put_object("batttrack", file.filename, file.file, file_size)
    return {
        "image_url": "http://119.59.102.68:9000/batttrack/" + ret._object_name
    }

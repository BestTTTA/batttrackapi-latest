"# batttrackapi-latest" 

# start minio
docker run ^
  -p 9000:9000 ^
  -p 9001:9001 ^
  --name minio1 ^
  -v //d/minio/data:/data ^
  -e MINIO_ROOT_USER=ROOTUSER ^
  -e MINIO_ROOT_PASSWORD=CHANGEME123 ^
  quay.io/minio/minio server /data --console-address ":9001"

# install package 
pip install minio
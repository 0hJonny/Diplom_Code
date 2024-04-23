import json
import os
import io
import minio
from minio.error import S3Error as ResponseError


class MinioClient(minio.Minio):
    def __init__(self, host=None, access_key=None, secret_key=None):
        host = f"{host or os.getenv('MINIO_HOST')}:9000"
        access_key = access_key or os.getenv('MINIO_USER')
        secret_key = secret_key or os.getenv('MINIO_PASSWORD')
        super().__init__(host, access_key, secret_key, secure=False)
    
    # Метод для загрузки изображения из файла
    def upload_image_from_file(self, bucket_name, object_name, file_path):
        try:
            if not self.bucket_exists(bucket_name):
                self._ensure_bucket_exists(bucket_name)
            self.fput_object(bucket_name, object_name, file_path)
            # print("Изображение успешно загружено в Minio")
        except ResponseError as err:
            return None
            # print(err)
    
    # Метод для загрузки изображения из байтов
    def upload_image_from_bytes(self, bucket_name, object_name, data):
        try:
            data_stream = io.BytesIO(data)
            if not self.bucket_exists(bucket_name):
                self._ensure_bucket_exists(bucket_name)
            self.put_object(bucket_name, object_name, data_stream, length=len(data))
            # print("Изображение успешно загружено в Minio")
        except ResponseError as err:
            return None
            # print(err)
    
    # Метод для получения URL изображения
    def get_image_url(self, bucket_name, object_name, expires=604800):  # По умолчанию URL будет действителен 7 дней
        try:
            url = self.presigned_get_object(bucket_name, object_name, expires=expires)
            # print("URL для изображения:", url)
            return url
        except ResponseError as err:
            return None
            # print(err)

    def _ensure_bucket_exists(self, bucket_name):
        try:
            self.make_bucket(bucket_name, object_lock=False)
        except ResponseError as err:
            if err.code != 'BucketAlreadyOwnedByYou':
                raise
        policy = {
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
                    "Resource": f"arn:aws:s3:::{bucket_name}",
                },
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*",
                },
            ],
        }
        self.set_bucket_policy(bucket_name, json.dumps(policy))

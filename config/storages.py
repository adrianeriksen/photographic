import os

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = os.environ["MEDIA_BUCKET_NAME"]


class StaticStorage(S3Boto3Storage):
    bucket_name = os.environ["STATIC_BUCKET_NAME"]

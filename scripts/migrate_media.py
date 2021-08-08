import argparse
import boto3
import mimetypes
import os

mimetypes.init()

parser = argparse.ArgumentParser(description="Migrate media resources to S3 compatible object store.")

parser.add_argument("source")
parser.add_argument("region")
parser.add_argument("bucket")

args = parser.parse_args()

source_dir = args.source
region_name = args.region
bucket = args.bucket
endpoint_url = f"https://{region_name}.digitaloceanspaces.com"

client = boto3.client("s3",
                      region_name=region_name,
                      endpoint_url=endpoint_url)

files = os.listdir(source_dir)

for file in files:
    full_path = source_dir + "/" + file

    mimetype, _ = mimetypes.guess_type(full_path)

    if mimetype:
        config = {
            "ACL": "public-read",
            "ContentType": mimetype
        }
        client.upload_file(full_path, bucket, file, config)
        print("Copying file", full_path, "to bucket", bucket)

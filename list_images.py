import boto3
import json
import os

s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']  # Get bucket name from environment variable


def lambda_handler(event, context):
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    images = []

    if 'Contents' in response:
        for item in response['Contents']:
            key = item['Key']
            if key.startswith("thumbnails/"):
                continue
            thumbnail_key = f"thumbnails/{key}"
            images.append({
                'image': f"s3://{BUCKET_NAME}/{key}",
                'thumbnail': f"s3://{BUCKET_NAME}/{thumbnail_key}"
            })

    return {
        'statusCode': 200,
        'body': json.dumps(images),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
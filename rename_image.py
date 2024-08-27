import boto3
import json
import os

s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']  # Get bucket name from environment variable


def lambda_handler(event, context):
    body = json.loads(event['body'])
    old_name = body['old_name']
    new_name = body['new_name']

    s3_client.copy_object(
        Bucket=BUCKET_NAME,
        CopySource={'Bucket': BUCKET_NAME, 'Key': old_name},
        Key=new_name
    )

    s3_client.delete_object(Bucket=BUCKET_NAME, Key=old_name)

    old_thumbnail_key = f"thumbnails/{old_name}"
    new_thumbnail_key = f"thumbnails/{new_name}"

    s3_client.copy_object(
        Bucket=BUCKET_NAME,
        CopySource={'Bucket': BUCKET_NAME, 'Key': old_thumbnail_key},
        Key=new_thumbnail_key
    )

    s3_client.delete_object(Bucket=BUCKET_NAME, Key=old_thumbnail_key)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f"Renamed {old_name} to {new_name} and corresponding thumbnail."
        }),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
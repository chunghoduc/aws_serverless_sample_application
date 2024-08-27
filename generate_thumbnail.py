import boto3
from PIL import Image
import io
import os

s3_client = boto3.client('s3')
THUMBNAIL_BUCKET = os.environ['THUMBNAIL_BUCKET']  # Get thumbnail bucket from environment variable
THUMBNAIL_SIZE = (128, 128)


def lambda_handler(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']

    if source_key.startswith("thumbnails/"):
        return

    image_object = s3_client.get_object(Bucket=source_bucket, Key=source_key)
    image_content = image_object['Body'].read()

    image = Image.open(io.BytesIO(image_content))
    image.thumbnail(THUMBNAIL_SIZE)

    thumbnail_buffer = io.BytesIO()
    image.save(thumbnail_buffer, format=image.format)
    thumbnail_buffer.seek(0)

    destination_key = f"thumbnails/{source_key}"

    s3_client.put_object(Bucket=THUMBNAIL_BUCKET, Key=destination_key, Body=thumbnail_buffer,
                         ContentType=image_object['ContentType'])

    return {
        'statusCode': 200,
        'body': f'Thumbnail created at {THUMBNAIL_BUCKET}/{destination_key}'
    }
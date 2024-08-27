import os
import boto3
from botocore.exceptions import ClientError
from PIL import Image
import io

s3_client = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']


def list_images(event, context):
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='images/')
    images = []
    for obj in response.get('Contents', []):
        image_key = obj['Key']
        thumbnail_key = image_key.replace('images/', 'thumbnails/')
        images.append({
            'image': f's3://{bucket_name}/{image_key}',
            'thumbnail': f's3://{bucket_name}/{thumbnail_key}'
        })
    return {
        'statusCode': 200,
        'body': json.dumps(images)
    }


def generate_thumbnail(event, context):
    for record in event['Records']:
        s3_event = record['s3']
        bucket = s3_event['bucket']['name']
        key = s3_event['object']['key']
        if key.startswith('images/'):
            try:
                response = s3_client.get_object(Bucket=bucket, Key=key)
                image_data = response['Body'].read()
                with Image.open(io.BytesIO(image_data)) as img:
                    img.thumbnail((128, 128))
                    thumbnail_key = key.replace('images/', 'thumbnails/')
                    buffer = io.BytesIO()
                    img.save(buffer, 'JPEG')
                    buffer.seek(0)
                    s3_client.put_object(Bucket=bucket, Key=thumbnail_key, Body=buffer, ContentType='image/jpeg')
            except Exception as e:
                print(e)
    return {
        'statusCode': 200,
        'body': 'Thumbnail generated successfully'
    }


def rename_image(event, context):
    old_name = event['old_name']
    new_name = event['new_name']

    try:
        s3_client.copy_object(
            Bucket=bucket_name,
            CopySource=f'{bucket_name}/{old_name}',
            Key=new_name
        )
        s3_client.delete_object(Bucket=bucket_name, Key=old_name)

        old_thumbnail_name = old_name.replace('images/', 'thumbnails/')
        new_thumbnail_name = new_name.replace('images/', 'thumbnails/')

        s3_client.copy_object(
            Bucket=bucket_name,
            CopySource=f'{bucket_name}/{old_thumbnail_name}',
            Key=new_thumbnail_name
        )
        s3_client.delete_object(Bucket=bucket_name, Key=old_thumbnail_name)

        return {
            'statusCode': 200,
            'body': f'Renamed {old_name} to {new_name} and updated thumbnail'
        }

    except ClientError as e:
        print(e)
        return {
            'statusCode': 500,
            'body': 'Error renaming image'
        }
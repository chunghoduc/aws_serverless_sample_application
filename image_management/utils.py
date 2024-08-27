from PIL import Image
import io

def create_thumbnail(image_data):
    with Image.open(io.BytesIO(image_data)) as img:
        img.thumbnail((128, 128))
        buffer = io.BytesIO()
        img.save(buffer, 'JPEG')
        buffer.seek(0)
        return buffer
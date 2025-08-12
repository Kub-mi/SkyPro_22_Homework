from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError, ImageFile


ImageFile.LOAD_TRUNCATED_IMAGES = True

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 МБ
ALLOWED_CONTENT_TYPES = {'image/jpeg', 'image/png'}
ALLOWED_FORMATS = {'JPEG', 'PNG'}


def validate_image_file(uploaded_file):
    if not uploaded_file:
        return

    if uploaded_file.size > MAX_IMAGE_SIZE:
        raise ValidationError('Размер изображения не должен превышать 5 МБ.')

    try:
        with Image.open(uploaded_file) as img:
            if img.format not in ALLOWED_FORMATS:
                raise ValidationError('Допустимые форматы: JPEG или PNG.')
    except UnidentifiedImageError:
        raise ValidationError('Файл не является корректным изображением JPEG/PNG.')
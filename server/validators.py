from PIL import Image
import os
from django.core.exceptions import ValidationError

def validate_icon_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(f"Icon size should be less than or equal to 70x70 {img.size}")
            


def validate_image_file_exstension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Invalid file extension, only jpg/jpeg/png/gif files are allowed')
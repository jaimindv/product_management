import os
import uuid

from django.conf import settings


def get_product_photo_random_filename(instance, filename):
    """
    Generate a random filename for product photos.

    Args:
        instance: The instance of the model.
        filename: The original filename.

    Returns:
        str: The formatted random filename.
    """
    extension = os.path.splitext(filename)[1]
    return "{}/{}{}".format(settings.PRODUCT_PHOTOS, uuid.uuid4(), extension)

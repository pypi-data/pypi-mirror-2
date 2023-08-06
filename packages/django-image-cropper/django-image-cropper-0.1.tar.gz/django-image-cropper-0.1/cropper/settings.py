from django.db import settings
from cropper.defaults import upload_success, crop_success

ROOT = getattr(settings, 'CROPPER_ROOT', 'cropped/').rstrip('/')
MAX_WIDTH  = getattr(settings, 'CROPPER_MAX_WIDTH',  1680)
MAX_HEIGHT = getattr(settings, 'CROPPER_MAX_HEIGHT', 1024)

UPLOAD_SUCCESS = upload_success
CROP_SUCCESS   = crop_success
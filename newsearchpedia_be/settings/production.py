from .base import *
DEBUG = False  # 로컬에서 True 프로덕션에선 False
ALLOWED_HOSTS = ['18.223.237.251']

# 프로덕션만?
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'

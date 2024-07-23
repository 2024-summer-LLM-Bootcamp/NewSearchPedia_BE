from .base import *

ALLOWED_HOSTS = ['*']

# CORS 설정 - whitelist 에 추가된 주소 접근 허용
CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:5173', 'http://localhost:5173']
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000',
                        'http://127.0.0.1:5173', 'http://localhost:5173']

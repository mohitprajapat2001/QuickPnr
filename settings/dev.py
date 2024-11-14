from settings.base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = [
    "*",
    "127.0.0.1",
    "localhost",
    "http://localhost:3000",
    "http://192.168.0.31:3000",
]


# Cors Allowed Origin
# =====================================================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://192.168.0.31:3000",
]
CORS_ALLOW_CREDENTIALS = True

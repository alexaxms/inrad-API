from .default import *
DEBUG = True
ALLOWED_HOSTS = "*"
# Cookie settings
CSRF_COOKIE_DOMAIN = '.musicmania.cl'
SESSION_COOKIE_DOMAIN = '.musicmania.cl'
# Set flags for session and csrf cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    '.musicmania.cl'
]
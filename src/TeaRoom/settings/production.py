from .base import *

# Destination of error alerts
ADMINS = (
    ("Elena", "elena.graverini@cern.ch"),
    #    ("Barbara", "barbara.storaci@cern.ch"),
    ("Marco", "mtresch@physik.uzh.ch"),
    ("Andreas", "weiden@physik.uzh.ch"),
)

# Send a notification to the managers every time
# somebody ends up onto a 404 with a non-empty
# referrer (i.e. a broken link)
SEND_BROKEN_LINK_EMAILS = True
MANAGERS = ADMINS
ALLOWED_HOSTS = [
    'da.physik.uzh.ch',
    'da',
    'marder.physik.uzh.ch',
]
# STATIC_ROOT = join(BASE_DIR, 'static')

# Try to use only HTTPS
# (see: https://docs.djangoproject.com/en/1.10/topics/security/#security-recommendation-ssl
# and:
# http://stackoverflow.com/questions/8015685/how-to-enable-https-in-django-auth-generated-pages
# )
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

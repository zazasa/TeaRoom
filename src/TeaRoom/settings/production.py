from .base import *

# Destination of error alerts
ADMINS = (
    ("Elena", "elena.graverini@cern.ch"),
#    ("Barbara", "barbara.storaci@cern.ch"),
#    ("Marco", "mtresch@physik.uzh.ch"),
)

# Send a notification to the managers every time
# somebody ends up onto a 404 with a non-empty
# referrer (i.e. a broken link)
SEND_BROKEN_LINK_EMAILS = True
MANAGERS = ADMINS
ALLOWED_HOSTS = [
    'marder.physik.uzh.ch',
]

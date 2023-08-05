# Django settings for comsat.

import os.path
_path = os.path.dirname(__file__)

# Add third party libraries
import sys
sys.path = [os.path.join(_path,'third_party','lib')] + sys.path

from secrets import DEBUG, RUNSCRIPT_DEBUG
TEMPLATE_DEBUG = DEBUG
JSON_DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('Jason B. Alonso', 'jalonso@manicsages.org'),
)

MANAGERS = ADMINS

from secrets import DATABASE_ENGINE, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, LOCAL_APPS, EXTRAS

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

from secrets import SITE_ID

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(_path, 'static', 'media')
STATIC_ROOT = os.path.join(_path, 'static')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
from secrets import SECRET_KEY, SESSION_COOKIE_DOMAIN

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

try:
        from secrets import ROOT_URLCONF
except:
        ROOT_URLCONF = 'manicbots.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(_path, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admindocs',
#    'django.contrib.markup',
) + LOCAL_APPS

# STOMP configuration
STOMP_HOSTS = (
        ('localhost',61613),
)
STOMP_USERNAME = None
STOMP_PASSWORD = None

# DjChat client configuration
DJCHAT_TOUCH_INTERVAL = 60

# Daemon channels
ECHOCHAMBER_SOURCE = '/queue/djchat.echo'
DJCHAT_ROOM_PREFIX = '/topic/djchat.room.'
DJCHAT_BROADCAST = '/topic/djchat.broadcast'
INSTANTREPLAY_SOURCE = '/queue/replay.control'

# TheOneChat configuration
THEONECHAT_ROOM = 'TheOneChat'

# Command Engine configuration
CONTROL_ROOMS = ('OperationsControl',)

# DjIRC configuration
## for single channel
DJIRC_NICK = 'DjIrc'
DJIRC_SERVER = 'irc.chatspike.net'
DJIRC_CHANNEL = '#djirc'

## for dedicated server
DJIRC_D_NICK = 'DjIrc'
DJIRC_D_SERVER = 'irc.manicsages.org'
DJIRC_D_CHAN_POLL = 5
DJIRC_D_USER_POLL = 30

# MoneyBot configuration
MONEYBOT_HANDLE = 'MoneyBot'
MONEYBOT_ROOMS = ('Treasury',)

# Kerby configuration
KERBY_KDC_QUEUE = '/queue/kerby.kdc'

# EditGrid configuration
EDITGRID_COMMAND_QUEUE = '/queue/editgrid.command'
EDITGRID_AUTH_INTERVAL = 60*60

# GeckoBot configuration
GECKOBOT_HANDLE = 'GeckoBot'
GECKOBOT_LOG_ROOM = CONTROL_ROOMS[0]
GECKOBOT_CHANGES_ROOM = 'Special:RecentChanges'
GECKOBOT_POLL_INTERVAL = 5
GECKOBOT_WARN_TIMEOUT  = 10
GECKOBOT_POLL_TIMEOUT  = 30

# Balancer configuration
BALANCER = {
        'host_template': 'http://%s.%d.comsat.manicsages.org/%s',
        'min_id': 0,
        'max_id': 1,
}

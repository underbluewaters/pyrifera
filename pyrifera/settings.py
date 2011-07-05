# Django settings for pyrifera project.

from lingcod.common.default_settings import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'pyrifera',
        'USER': 'postgres',
    }
}

TIME_ZONE = 'America/Vancouver'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

ROOT_URLCONF = 'pyrifera.urls'

TEMPLATE_DIRS = ( os.path.realpath(os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/')), )

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$_b-5e9rt!m!k^_)h4h-y54jqnumgfg$-vgk-@(=02f4-6#(u$'

INSTALLED_APPS += ( 'monitoring', 'kfm', 'haystack')
# 
# MPA_CLASS = 'mlpa.models.Mpa'
# ARRAY_CLASS = 'mlpa.models.MpaArray'
# MPA_FORM = 'mlpa.forms.MpaForm'
# ARRAY_FORM = 'mlpa.forms.ArrayForm'

HAYSTACK_SITECONF = 'monitoring.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = 'haystack_index'
HAYSTACK_INCLUDE_SPELLING = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

from settings_local import *

APP_NAME = 'NPS Kelp Forest Monitoring Data Viewer'
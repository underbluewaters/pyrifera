# Django settings for pyrifera project.

from lingcod.common.default_settings import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'pyrifera'
DATABASE_USER = 'postgres'

TIME_ZONE = 'America/Vancouver'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

ROOT_URLCONF = 'pyrifera.urls'

TEMPLATE_DIRS = ( os.path.realpath(os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/')), )

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$_b-5e9rt!m!k^_)h4h-y54jqnumgfg$-vgk-@(=02f4-6#(u$'

INSTALLED_APPS += ( 'monitoring', 'kfm', 'pisco_intertidal')
# 
# MPA_CLASS = 'mlpa.models.Mpa'
# ARRAY_CLASS = 'mlpa.models.MpaArray'
# MPA_FORM = 'mlpa.forms.MpaForm'
# ARRAY_FORM = 'mlpa.forms.ArrayForm'

from settings_local import *
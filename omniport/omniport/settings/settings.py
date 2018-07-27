"""
This file extends the base settings with settings loaded from the YAML
configuration files.
"""

import yaml

from omniport.settings.base import *

# Site ID helps in loading site-specific configuration
SITE_ID = int(os.getenv('SITE_ID', '0'))

# Read the configuration files from the ``configuration`` directory

base_config_file = open(os.path.join(
    CONFIGURATION_DIR,
    'base.yml'
))
base_configuration = yaml.load(base_config_file)

site_config_file = open(os.path.join(
    CONFIGURATION_DIR,
    'sites',
    f'site_{SITE_ID}.yml'
))
site_configuration = yaml.load(site_config_file)

# Note that site_configuration overrides base_configuration
configuration = {**base_configuration, **site_configuration}

# Branding

branding = configuration.get('branding', {})

institute = branding.get('institute', {})

INSTITUTE_NAME = institute.get('name', 'Institute')

INSTITUTE_HOME_PAGE = institute.get(
    'homePage',
    'https://dhruvkb.github.io/'
)

maintainers = branding.get('maintainers', {})

MAINTAINERS_NAME = maintainers.get('name', 'Dhruv Bhanushali')

MAINTAINERS_HOME_PAGE = maintainers.get(
    'homePage',
    'https://dhruvkb.github.io/'
)

# Site

SITE = configuration.get('site', {})

SITE_NAME = SITE.get('name', f'site_{SITE_ID}')

SITE_VERBOSE_NAME = SITE.get('verboseName', f'Omniport Site {SITE_ID}')

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASE = configuration.get('database', {})

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': DATABASE.get('host', 'database'),
        'NAME': DATABASE.get('name', 'omniport_database'),
        'USER': DATABASE.get('user', 'omniport_user'),
        'PASSWORD': DATABASE.get('password', 'omniport_password'),
        'PORT': DATABASE.get('port', 5432),
    },
}

# Channel layer
# http://channels.readthedocs.io/en/latest/topics/channel_layers.html

CHANNEL_LAYER = configuration.get('channelLayer', {})

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                (
                    CHANNEL_LAYER.get('host', 'channel-layer'),
                    CHANNEL_LAYER.get('port', 6379),
                )
            ],
        },
    },
}

# CORS configuration

cors = configuration.get('cors', {})

CORS_ALLOW_CREDENTIALS = cors.get('allowCredentials', False)

CORS_ORIGIN_WHITELIST = cors.get('originWhitelist', list())

CORS_ORIGIN_ALLOW_ALL = cors.get('originAllowAll', False)

# Network rings

NETWORK_RINGS = configuration.get('networkRings')

IP_ADDRESS_PATTERNS = dict()

ip_address_patterns = configuration.get('ipAddressPatterns')
for ip_address_pattern in ip_address_patterns:
    ring_name = ip_address_pattern.get('ringName')
    patterns = ip_address_pattern.get('patterns')
    IP_ADDRESS_PATTERNS[ring_name] = patterns

# Internationalisation and localisation

I18N = configuration.get('i18n', {})

LANGUAGE_CODE = I18N.get('languageCode', 'en-gb')

TIME_ZONE = I18N.get('timeZone', 'Asia/Kolkata')

# This key, as implied by the name, should be a well-protected secret
SECRET_KEY = configuration.get(
    'secretKey',
    # For the love of all that is holy, change this in production
    'placeholder_19kbufifr&(r5i8qv&i-e^d08ma#1s0kgdi(_lce9r301teck-'
)

# This variable should be True in testing environments and False otherwise
DEBUG = configuration.get('debug', False)

if DEBUG:
    # The list of hosts to which this application will respond
    ALLOWED_HOSTS = ['*']
    # The list of apps whose URLs will be loaded in this app
    allowed_apps = '__all__'
else:
    # The list of hosts to which this application will respond
    ALLOWED_HOSTS = configuration.get('allowedHosts', [])
    # The list of apps whose URLs will be loaded in this app
    allowed_apps = configuration.get('allowedApps', '__all__')

for app in DISCOVERY.get('apps').get('apps'):
    if allowed_apps == '__all__' or app.get('name') in allowed_apps:
        app['isAllowed'] = True
    else:
        app['isAllowed'] = False
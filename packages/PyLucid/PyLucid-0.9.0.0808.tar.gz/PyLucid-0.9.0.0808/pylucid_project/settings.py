# coding: utf-8

"""
    PyLucid.settings
    ~~~~~~~~~~~~~~~~

    Django settings for the PyLucid project.

    IMPORTANT:
        You should not edit this file!
        Owerwrite settings with a local settings file:
            local_settings.py

    Here are not all settings predifined you can use. Please look at the
    django documentation for a full list of all items:
        http://www.djangoproject.com/documentation/settings/

    :copyleft: 2009-2011 by the PyLucid team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import os
import sys


try:
    #from django_tools.utils import info_print;info_print.redirect_stdout()
    import django
    import dbpreferences
    import django_tools
    import pylucid_project
    from pylucid_project.system.plugin_setup_info import PyLucidPluginSetupInfo
except Exception, e:
    import traceback
    sys.stderr.write(traceback.format_exc())
    raise

try:
    import south
except ImportError:
    _south_exists = False
else:
    _south_exists = True


# Used by a few dynamic settings:
if "runserver" in sys.argv:
    RUN_WITH_DEV_SERVER = True
else:
    RUN_WITH_DEV_SERVER = False


PYLUCID_BASE_PATH = os.path.abspath(os.path.dirname(pylucid_project.__file__))
#print "PYLUCID_BASE_PATH:", PYLUCID_BASE_PATH
#PYLUCID_PLUGINS_ROOT = os.path.abspath(os.path.dirname(pylucid_plugins.__file__))

#______________________________________________________________________________
# SYS PATH SETUP

_path_list = (
#    PYLUCID_PLUGINS_ROOT,
    PYLUCID_BASE_PATH,
    os.path.join(PYLUCID_BASE_PATH, "apps")
)
for path in _path_list:
    if path not in sys.path:
        sys.path.insert(0, path)

#______________________________________________________________________________
# DEBUGGING

DEBUG = False

# Append all SQL queries into the html page. (Works only if DEBUG==True)
# Should allways be False. It's only for developing! 
SQL_DEBUG = False

# See if request.PYLUCID attributes attached or changes (Works only if DEBUG==True)
# See also: http://www.pylucid.org/permalink/133/pylucid-objects#DEBUG
# Should allways be False. It's only for developing! 
PYLUCID_OBJECTS_DEBUG = False

# We must set a defaul DB settings here, otherwise managment commands doesn't work.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'PleaseOverwrite_DATABASES_settings',
    }
}

SITE_ID = 1 # Can be changed in local_settings


ROOT_URLCONF = 'pylucid_project.urls'

MIDDLEWARE_CLASSES = (
    'pylucid_project.middlewares.ip_ban.IPBanMiddleware',

    'django_tools.local_sync_cache.LocalSyncCacheMiddleware.LocalSyncCacheMiddleware',

    # Insert a statistic line into the generated page:
    'pylucid_project.middlewares.pagestats.PageStatsMiddleware',

    'django.middleware.cache.UpdateCacheMiddleware',

    # From http://code.google.com/p/django-tools/
    'django_tools.middlewares.ThreadLocal.ThreadLocalMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'dbpreferences.middleware.DBPreferencesMiddleware',

    'pylucid_project.middlewares.pylucid_objects.PyLucidMiddleware',

    # slow down the django developer server
    # From http://code.google.com/p/django-tools/
#    'django_tools.middlewares.SlowerDevServer.SlowerDevServerMiddleware',

    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',

    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',

    # Insert a html link anchor to all headlines:
    'pylucid_project.middlewares.headline_anchor.HeadlineAnchorMiddleware',

    # Set django message level by user type and system preferences:
    'pylucid_project.middlewares.message_level.MessageLevelMiddleware',
)


# Add stack information to every messages, but only if..
#     ...settings.DEBUG == True
# or
#     ...settings.MESSAGE_DEBUG == True
MESSAGE_STORAGE = "django_tools.utils.messages.StackInfoStorage"


# initialized all pylucid plugins
PYLUCID_PLUGIN_SETUP_INFO = PyLucidPluginSetupInfo(
    plugin_package_list=(
        (PYLUCID_BASE_PATH, "pylucid_project", "pylucid_plugins"),
        (PYLUCID_BASE_PATH, "pylucid_project", "external_plugins"),
    ),
#    verbose=True
    verbose=False
)

TEMPLATE_DIRS = (
    os.path.join(PYLUCID_BASE_PATH, "apps/pylucid/templates/"),
    os.path.join(PYLUCID_BASE_PATH, "apps/pylucid_admin/templates/"),
    os.path.join(PYLUCID_BASE_PATH, "apps/pylucid_update/templates/"),

    os.path.join(os.path.abspath(os.path.dirname(django_tools.__file__)), "templates/"),
    os.path.join(os.path.abspath(os.path.dirname(dbpreferences.__file__)), "templates/"),
    os.path.join(os.path.abspath(os.path.dirname(django.__file__)), "contrib/admin/templates"),
)
# Add all templates subdirs from all existing PyLucid plugins
TEMPLATE_DIRS += PYLUCID_PLUGIN_SETUP_INFO.template_dirs
#print "settings.TEMPLATE_DIRS:\n", "\n".join(TEMPLATE_DIRS)

TEMPLATE_LOADERS = (
    'dbtemplates.loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# A tuple of callables that are used to populate the context in RequestContext.
# These callables take a request object as their argument and return a
# dictionary of items to be merged into the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "pylucid_project.apps.pylucid.context_processors.pylucid",
)

# Template debug should be off, because you didn't see a good debug page, if the error
# is in a lucidTag plugin view!
# Note that Django only displays fancy error pages if DEBUG is True!
TEMPLATE_DEBUG = False
#TEMPLATE_DEBUG = True

if DEBUG:
    # Display invalid (e.g. misspelled, unused) template variables
    # http://www.djangoproject.com/documentation/templates_python/#how-invalid-variables-are-handled
    # http://www.djangoproject.com/documentation/settings/#template-string-if-invalid
    # But note: Some django admin stuff is broken if TEMPLATE_STRING_IF_INVALID != ""
    # see also: http://code.djangoproject.com/ticket/3579
    # A work-a-round for this lives in ./pylucid_project/apps/pylucid_admin/admin.py 
    TEMPLATE_STRING_IF_INVALID = "XXX INVALID TEMPLATE STRING '%s' XXX"
#    from django_tools.template import warn_invalid_template_vars
#    warn_invalid_template_vars.add_warning()



INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.redirects',

    # PyLucid own apps:
    'pylucid_project.apps.pylucid',
    'pylucid_project.apps.pylucid_admin',
    'pylucid_project.apps.pylucid_update', # Only needed for v0.8 users

    # external apps shipped and used with PyLucid:
    'dbpreferences',
    'dbtemplates',
    'reversion',
    'tagging',
)
if _south_exists: # Add south if it can be imported above
    INSTALLED_APPS += ("south",)

# Add all existing PyLucid plugins
INSTALLED_APPS += PYLUCID_PLUGIN_SETUP_INFO.installed_plugins
#print "settings.INSTALLED_APPS:", "\n".join(INSTALLED_APPS)

COMMENTS_APP = "pylucid_project.pylucid_plugins.pylucid_comments"

#http://docs.djangoproject.com/en/dev/ref/settings/#setting-TEST_RUNNER
#Default: 'django.test.simple.run_tests'
TEST_RUNNER = 'pylucid_project.tests.test_tools.test_runner.PyLucidTestRunner'

#_____________________________________________________________________________
# PyLucid own settings

# Add app settings
try:
    from pylucid_project.apps.pylucid import app_settings as PYLUCID
    from pylucid_project.apps.pylucid_admin import app_settings as ADMIN
except Exception, e:
    import traceback
    sys.stderr.write(traceback.format_exc())
    raise


# http://www.djangoproject.com/documentation/authentication/#other-authentication-sources
AUTHENTICATION_BACKENDS = (
    "pylucid.system.auth_backends.SiteAuthBackend",
    "pylucid.system.auth_backends.SiteSHALoginAuthBackend",
#    "django.contrib.auth.backends.ModelBackend",
#    "pylucid_project.pylucid_plugins.auth.auth_backend.JS_SHA_Backend",
)
# http://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users
AUTH_PROFILE_MODULE = "pylucid.UserProfile"

#_____________________________________________________________________________
# STATIC FILES
# http://www.djangoproject.com/documentation/static_files/

# Serve static files for the development server?
# Using this method is inefficient and insecure.
# Do not use this in a production setting. Use this only for development.
if RUN_WITH_DEV_SERVER:
    SERVE_STATIC_FILES = True
else:
    SERVE_STATIC_FILES = False


# Note: Every URL/path...
# ...must be a absolute path.
# ...must have a trailing slash.

# Absolute _local_filesystem_path_ to the directory that holds media.
#     Example-1: "./media/" (default)
#     Example-2: "/home/foo/htdocs/media/"
MEDIA_ROOT = os.path.join(PYLUCID_BASE_PATH, "media") + "/"

# URL that handles the media served from MEDIA_ROOT.
#     Example-1: "/media/" (default)
#     Examlpe-2: "http://other_domain.net/media/"
#     Example-3: "http://media.your_domain.net/"
MEDIA_URL = "/media/"

# URL prefix for admin media -- CSS, JavaScript and images.
#     Examples-1: "/django/contrib/admin/media/" (default)
#     Examples-2: "http://other_domain.net/media/django/"
#     Examples-3: "http://django.media.your_domain.net/"
ADMIN_MEDIA_PREFIX = "/django/contrib/admin/media/"

ADMIN_URL_PREFIX = 'admin'
PYLUCID_ADMIN_URL_PREFIX = 'pylucid_admin'

LOGIN_REDIRECT_URL = "/%s/" % ADMIN_URL_PREFIX
LOGIN_URL = "/%s/" % ADMIN_URL_PREFIX
LOGOUT_URL = "/?%s" % PYLUCID.AUTH_LOGOUT_GET_VIEW


# TODO: must be used ;)
SLUG_BLACKLIST = (
    MEDIA_URL.strip("/").split("/", 1)[0],
    ADMIN_URL_PREFIX, PYLUCID_ADMIN_URL_PREFIX, PYLUCID.HEAD_FILES_URL_PREFIX,
)

# Prefix in filename, used for page templates
SITE_TEMPLATE_PREFIX = 'site_template'

# Prefix in filename, used for page stylesheet
SITE_STYLE_PREFIX = 'site_stylesheet'


# The PyLucid install instrucion page:
INSTALL_HELP_URL = "http://pylucid.org/_goto/186/v0-9-testing/"

# Django can't handling time zone very good.
# The Django default TIME_ZONE is 'America/Chicago' (Central Standard Time Zone, (CST), UTC-6)
# but this is not the best choice.
# We set it to "UTC" (same as Greenwich Mean Time, GMT-0, without daylight-saving time)
# All datetime (e.g. model createtime) would be stored in UTC.
# See also: http://groups.google.com/group/django-developers/browse_thread/thread/4ca560ef33c88bf3
TIME_ZONE = "UTC"

# Default system language.
# (Default from django is en-us, but this doesn't exist in PyLucid installed data)
LANGUAGE_CODE = "en"

#_______________________________________________________________________________
# dbtemplates settings
# http://packages.python.org/django-dbtemplates/overview.html#settings

# Use django-reversion ?
DBTEMPLATES_USE_REVERSION = True

#_______________________________________________________________________________
# settings for local_sync_cache from django-tools

if DEBUG and RUN_WITH_DEV_SERVER:
    LOCAL_SYNC_CACHE_DEBUG = True
else:
    LOCAL_SYNC_CACHE_DEBUG = False

LOCAL_SYNC_CACHE_BACKEND = "local_sync_cache"

#_______________________________________________________________________________

# Set the Django cache system.
# The LocMemCache isn't memory-efficient. Should be changed in local_settings.py !
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'PyLucid-default-cache',
    },
    'dbtemplates': { # http://django-dbtemplates.readthedocs.org/en/latest/advanced/#caching
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'PyLucid-dbtemplates-cache',
    },
    LOCAL_SYNC_CACHE_BACKEND: { # https://github.com/jedie/django-tools/blob/master/django_tools/local_sync_cache/local_sync_cache.py
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'PyLucid-local_sync-cache',
    },
}
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

#_______________________________________________________________________________


try:
    from local_settings import *
except ImportError, err:
    if str(err) == "No module named local_settings":
        msg = (
            "There is no local_settings.py file in '%s' !"
            " (Original error was: %s)\n"
        ) % (os.getcwd(), err)
        sys.stderr.write(msg)
        #from django.core.exceptions import ImproperlyConfigured
        #raise ImproperlyConfigured(msg)
    else:
        raise



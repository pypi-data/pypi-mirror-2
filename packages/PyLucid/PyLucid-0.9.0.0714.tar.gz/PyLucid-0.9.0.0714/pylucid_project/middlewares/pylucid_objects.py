# coding: utf-8

import traceback

from django.conf import settings
from django.contrib.redirects.models import Redirect
from django.http import Http404
from django.utils.encoding import smart_str

from pylucid_project.apps.pylucid.models import LogEntry
from pylucid_project.apps.pylucid.system import pylucid_objects


class PyLucidMiddleware(object):
    def process_request(self, request):
        """ Add PyLucid objects to the request object """
        request.PYLUCID = pylucid_objects.PyLucidRequestObjects(request)

    def process_exception(self, request, exception):
        if isinstance(exception, Http404): # Handle 404 page not found errors

            # Get the system preferences
            sys_pref = request.PYLUCID.preferences
            sys_pref_form = request.PYLUCID.preferences_form

            log404_verbosity = sys_pref.get("log404_verbosity", sys_pref_form.LOG404_NOREDIRECT)

            if log404_verbosity == sys_pref_form.LOG404_NOTHING:
                # Don't log 'Page not found' errors.
                return

            # Check if there exist a django.contrib.redirects entry for this url
            path = request.get_full_path()
            try:
                r = Redirect.objects.get(site__id__exact=settings.SITE_ID, old_path=path)
            except Redirect.DoesNotExist:
                LogEntry.objects.log_action(
                    app_label="pylucid", action="PyLucidMiddleware.process_exception()",
                    message="Redirect for %r doesn't exist." % path
                )
                return
            else:
                # Redirect entry exist
                if log404_verbosity == sys_pref_form.LOG404_NOREDIRECT:
                    # Log only 'Page not found' if no redirect for the url exists.
                    return

                LogEntry.objects.log_action(
                    app_label="pylucid", action="PyLucidMiddleware.process_exception()",
                    message="Redirect for %r exist." % path
                )
                return

        # cut exception message text to LogEntry.message max_length, to get no "Data truncated..." warning
        message = smart_str(exception, errors='replace')[:255]

        LogEntry.objects.log_action(
            app_label="pylucid", action="PyLucidMiddleware.process_exception()", message=message,
            long_message=traceback.format_exc()
        )

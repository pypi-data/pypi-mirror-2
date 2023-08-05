# coding: utf-8

"""
    PyLucid OpenStreetMap plugin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Last commit info:
    ~~~~~~~~~
    $LastChangedDate:$
    $Rev:$
    $Author: JensDiemer $

    :copyleft: 2010 by the PyLucid team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details
"""

from django.contrib import messages
from django.core import urlresolvers
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import signals
from django.template import TemplateDoesNotExist
from django.template.defaultfilters import slugify
from django.template.loader import find_template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

# http://code.google.com/p/django-tools/
from django_tools.middlewares import ThreadLocal

from pylucid_project.apps.pylucid.models import PageContent
from pylucid_project.apps.pylucid.markup.converter import apply_markup
from pylucid_project.apps.pylucid.models.base_models import AutoSiteM2M, UpdateInfoBaseModel

from StreetMap.preference_forms import PreferencesForm


class MapEntry(AutoSiteM2M, UpdateInfoBaseModel):
    TYPE_OSM = "O"
    TYPE_GOOGLE = "G"
    TYPE_CHOICES = ( # for self.map_type field
        (TYPE_OSM, 'OpenStreetMap'),
        (TYPE_GOOGLE, 'Google Maps'),
    )
    TEMPLATES = { # Used in views.py
        TYPE_OSM: "StreetMap/OpenStreetMap.html",
        TYPE_GOOGLE: "StreetMap/GoogleMaps.html",
    }
    LINK_TEMPLATE = { # Used in admin.py
        TYPE_OSM: "StreetMap/includes/OpenStreetMap_link.html",
        TYPE_GOOGLE: "StreetMap/includes/GoogleMaps_link.html",
    }
    
    name = models.SlugField(unique=True,
        help_text=_("Short name for lucidTag")
    )
    
    map_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=TYPE_OSM)
    template_name = models.CharField(max_length=128,null=True, blank=True,
        help_text=_(
            "Template path for this map."
            " (Optional, leave empty for default!"
        )
    )
    
    width = models.CharField(max_length=8,
        default="100%",
        help_text=_("Map width size")
    )
    height = models.CharField(max_length=8,
        default="400px",
        help_text=_("Map height size")
    )    
    
    lon = models.FloatField(
        help_text=_("map geographic longitude (vertically) coordinate"),
    )
    lat = models.FloatField(
        help_text=_("map geographic latitude (horizontally) coordinate"),
    )
    zoom = models.PositiveSmallIntegerField(
        default=12,
        help_text=_("Map zoom factor"),
    )
    
    marker_lon = models.FloatField(null=True, blank=True,
        help_text=_(
            "Text marker longitude (vertically) coordinate."
            " (Optional, leave empty to use the map centre.)"
        )
    )
    marker_lat = models.FloatField(null=True, blank=True,
        help_text=_(
            "Text marker latitude (horizontally) coordinate"
            " (Optional, leave empty to use the map centre.)"
        )
    )
    marker_width = models.PositiveIntegerField(
        default=180,
        help_text=_("Text marker width size")
    )
    marker_height = models.PositiveIntegerField(
        default=125,
        help_text=_("Text marker height size")
    )
    marker_text=models.TextField(null=True, blank=True,
        help_text=_(
            "Marker text."
            " (Optional, leave empty if no popup marker should be displayed.)"
        )
    )
    markup = models.IntegerField(max_length=1,
        help_text=_("Markup format used in marker text content."),
        default=PageContent.MARKUP_CREOLE,
        choices=PageContent.MARKUP_CHOICES
    )
    
    def check_google_api_key(self):
        if self.map_type == self.TYPE_GOOGLE:
            # Get preferences from DB
            pref_form = PreferencesForm()
            preferences = pref_form.get_preferences()
            if not preferences["google_maps_api_key"]:
                request = ThreadLocal.get_current_request()
                messages.warning(request, _(
                    "You must insert your google maps key into preferences!"
                    " Goto: Django admin site / Dbpreferences / StreetMap / edit preferences"
                ))

    def get_template_name(self):
        """ return default or user set template name """
        if self.template_name:
            return self.template_name
        else:
            map_type = self.map_type
            return self.TEMPLATES[map_type]

    def clean_fields(self, exclude):
        message_dict = {}

        if "template_name" not in exclude and self.template_name:
            try:
                find_template(self.template_name)
            except TemplateDoesNotExist, err:
                message_dict["template_name"] = [_("Template doesn't exist.")]
                
        self.check_google_api_key()

        if message_dict:
            raise ValidationError(message_dict)

    def get_html(self):
        """ return the marker_text as html """
        request = ThreadLocal.get_current_request()
        html = apply_markup(
            raw_content=self.marker_text,
            markup_no=self.markup, 
            request=request
        )
        # Needed for JavaScript:
        html = html.strip().replace("\n", "").replace('"', '\"')
        return mark_safe(html)
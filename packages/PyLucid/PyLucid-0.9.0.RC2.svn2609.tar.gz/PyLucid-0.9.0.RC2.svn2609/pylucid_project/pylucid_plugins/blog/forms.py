# -*- coding: utf-8 -*-

"""
    PyLucid blog forms
    ~~~~~~~~~~~~~~~~~~

    Forms for the blog.

    Last commit info:
    ~~~~~~~~~
    $LastChangedDate: 2009-11-05 16:43:36 +0100 (Do, 05. Nov 2009) $
    $Rev: 2349 $
    $Author: JensDiemer $

    :copyleft: 2008 by the PyLucid team, see AUTHORS for more details.
    :license: GNU GPL v2 or above, see LICENSE for more details
"""

from django import forms

# http://code.google.com/p/django-tools/
#from django_tools.forms_utils import LimitManyToManyFields

from blog.models import BlogEntry


class BlogEntryForm(forms.ModelForm):
    """
    Form for create/edit a blog entry.
    """
    class Meta:
        model = BlogEntry

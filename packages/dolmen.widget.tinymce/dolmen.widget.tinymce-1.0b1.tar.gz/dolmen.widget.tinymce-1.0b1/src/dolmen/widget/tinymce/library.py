# -*- coding: utf-8 -*-

from megrok import resource
from hurry.jquery import jquery
from hurry.tinymce import tinymce


class JqueryTinyMCE(resource.ResourceLibrary):
    resource.path('resources')
    resource.resource('jquery_tiny_mce.js', depends=[tinymce, jquery])

# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from manifesto.views import ManifestView


urlpatterns = patterns('',
    url(r'^cache\.manifest$', ManifestView.as_view(), name="cache_manifest"),
)

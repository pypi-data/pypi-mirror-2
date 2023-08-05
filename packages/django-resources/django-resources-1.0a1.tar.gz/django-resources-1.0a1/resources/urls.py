# django imports
from django.conf.urls.defaults import *

urlpatterns = patterns('resources.views',
   url(r'^create-css$', "create_css", name='create_css'),
   url(r'^create-javascript$', "create_javascript", name='create_javascript'),
   url(r'^create-resources$', "create_resources", name='create_resources'),
)
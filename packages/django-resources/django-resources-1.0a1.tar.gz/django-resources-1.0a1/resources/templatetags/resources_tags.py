# python imports
import os

# django imports
from django import template
from django.conf import settings
from django.core.cache import cache
from django.template.loader import render_to_string

# resources imports
from resources.utils import get_cached_object
from resources.config import CSS
from resources.config import JS
from resources.config import RESOURCES_DIRECTORY
from resources.models import Resource
from resources.models import MergedResource

register = template.Library()

@register.inclusion_tag('resources/resources.html', takes_context=True)
def css(context, group=None):
    """Returns HTML to embed generated css..
    
    **Parameters**
    
    group
        The group for which the CSS should be linked in.
    """
    resources = _get_resources(context, type=CSS, group=group)

    cache_key = "resources-css-%s" % group
    result = cache.get(cache_key)
    
    if result:
        return { "resources" : result }
    else:
        # Render the HTML here in order to cache it completely
        result = render_to_string("resources/css.html", resources)
        cache.set(cache_key, result)
        return { "resources" : result }

@register.inclusion_tag('resources/resources.html', takes_context=True)
def javascript(context, group=None):
    """Returns HTML to embed generated javascript. 

    **Parameters**
    
    group
        The group for which the javascript should be linked in.
    """
    resources = _get_resources(context, type=JS, group=group)

    cache_key = "resources-js-%s" % group    
    result = cache.get(cache_key)

    if result:
        return { "resources" : result }
    else:
        # Render the HTML here in order to cache it completely
        result = render_to_string("resources/javascript.html", resources)
        cache.set(cache_key, result)
        return { "resources" : result }

def _get_resources(context, type, group=None):
    MEDIA_URL = context.get("MEDIA_URL", "/")

    if getattr(settings, "RESOURCES_DEBUG", False):
        if group:        
            resources = Resource.objects.filter(type=type, group=group)
        else:
            resources = Resource.objects.filter(type=type)
        return {
            "MEDIA_URL" : MEDIA_URL,
            "resources" : resources,
        }
    else:
        if group:
            resources = list(MergedResource.objects.filter(type=type, group=group))
            resources.extend(Resource.objects.filter(type=type, merge=False, group=group))
        else:
            resources = list(MergedResource.objects.filter(type=type))
            resources.extend(Resource.objects.filter(type=type, merge=False))

        resources.sort(lambda a, b: cmp(a.position, b.position))

        return {
            "MEDIA_URL" : MEDIA_URL,
            "resources" : resources,
        }
# python imports
import datetime
import os
import re
import shutil

# django imports
from django.db import connection
from django.db.models import Count
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import _get_queryset

# resources imports
from resources.models import Resource
from resources.models import MergedResource
from resources.config import CSS
from resources.config import JS
from resources.config import RESOURCES_DIRECTORY

# cssutils imports
import cssutils
from cssutils import CSSParser

# jsmin imports
from jsmin import jsmin

def create_resources():
    """Creates merged and minified CSS and Javascript of registered resources.
    """
    create_css()
    create_javascript()

def url_replacer(url, resource):
    if url.startswith("/"):
        return url
    else:
        pos = resource.path.rfind("/")
        path = resource.path[0:pos]
        path = settings.MEDIA_URL + path + "/" + url
        path = re.sub("/+", "/", path)
        return path

def create_css():
    """Creates merged and minified CSS of registered CSS resources.
    """
    groups = get_groups(type=CSS)
    cssutils.ser.prefs.useMinified()

    for group in groups:
        cache.delete("resources-css-%s" % group)
        merged_resource, created = MergedResource.objects.get_or_create(type=CSS, group=group)

        max_position = 0
        text = ""
        for resource in Resource.objects.filter(type=CSS, group=group, merge=True):
            if resource.position > max_position:
                max_position = resource.position

            if resource.media:
                text += " @media %s { " % resource.media

            parser = CSSParser()
            sheet = parser.parseFile(settings.MEDIA_ROOT + resource.path)

            cssutils.replaceUrls(sheet, lambda url: url_replacer(url, resource))

            text += sheet.cssText

            if resource.media:
                text += " } "

        merged_resource.update(text, max_position)

def create_javascript():
    """Creates merged and minified javascript of registered Javascript
    resources.
    """
    cache.delete("resources-js")
    groups = get_groups(type=JS)

    for group in groups:
        cache.delete("resources-js-%s" % group)
        merged_resource, created = MergedResource.objects.get_or_create(type=JS, group=group)

        max_position = 0
        text = ""
        for resource in Resource.objects.filter(type=JS, group=group, merge=True):
            if resource.position > max_position:
                max_position = resource.position
            with open(settings.MEDIA_ROOT + resource.path, "r") as f:
                temp = f.read()

            if resource.minify:
                temp = jsmin(temp)

            text += temp + "\n"

        merged_resource.update(text, max_position)

def register_resource(path, type, merge=True, minify=True, group=None, position=None):
    """Registers a resource.

    **Parameters:**

    path
        The relative path (to MEDIA_URL) to the resource. Must be unique.

    type
        The type of the resource. One of resources.config.CSS,
        resources.config.JS

    merge
        If True the resource will be merged with other resources of the same
        group.

    minify
        If True the resource will be minified.

    group
        The group of the resource. Groups can be merged together and seperately
        included in the HTML page.

    position
        The position of the resource within its group. Lower positions come
        first within HTML.
    """
    resource, created = Resource.objects.get_or_create(path=path, type=type)
    resource.merge = merge
    resource.minify = minify
    resource.group = group
    if position:
        resource.position = position
    resource.save()

def unregister_resource(path):
    """Unregisters the resource.

    **Parameters:**

    path
        The unique path to the resource.
    """
    try:
        resource = Resource.objects.get(path=path)
    except Resource.DoesNotExist:
        pass
    else:
        resource.delete()

def get_cached_object(klass, *args, **kwargs):
    cache_key = "%s-%s" % (klass.__name__.lower(), kwargs.values()[0])
    object = cache.get(cache_key)
    if object is not None:
        return object

    queryset = _get_queryset(klass)

    try:
        object = queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
    else:
        cache.set(cache_key, object)
        return object

def reset():
    """Re-creates the resources directory.
    """
    MergedResource.objects.all().delete()
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, RESOURCES_DIRECTORY))
    create_directory()

def create_directory():
    """Creates resources directory.
    """
    try:
        os.mkdir(os.path.join(settings.MEDIA_ROOT, RESOURCES_DIRECTORY))
    except OSError:
        pass

# TODO: Use ORM
def get_groups(type):
    """Returns list of names of all groups.
    """
    cursor = connection.cursor()
    cursor.execute("""SELECT "group"
                      FROM resources_resource
                      WHERE type = %s
                      GROUP BY "group" """ % type)

    return [group[0] for group in cursor.fetchall()]
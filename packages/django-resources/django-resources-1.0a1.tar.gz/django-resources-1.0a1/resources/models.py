# python imports
import datetime
import os

# django imports
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _

# resources imports
from resources.config import CSS
from resources.config import RESOURCE_CHOICES
from resources.config import RESOURCES_DIRECTORY

class MergedResource(models.Model):
    """A merged resource out of one or more registered Resources.

    **Attibute:**

    last_updated
        The date the merged resources has been updated.

    type
        The type of resources which are merged.

    group
        The group resources which are merged.

    filename
        The current filename of the merged resource.

    position
        The position of the merged resource.

    """
    last_updated = models.DateTimeField(_("Last update"), blank=True, null=True)
    type = models.PositiveSmallIntegerField(_("Type"), choices=RESOURCE_CHOICES)
    group = models.CharField(_("Group"), blank=True, max_length=255)
    filename = models.CharField(_("Filename"), blank=True, max_length=40)
    position = models.PositiveIntegerField(default=10)

    def get_path(self):
        """Returns the full path to the resource.
        """
        return os.path.join(RESOURCES_DIRECTORY, self.filename)

    def update(self, text, position):
        """Creates a new resources file and sets text and timestamp.
        """
        import resources.utils
        resources.utils.create_directory()
        filename = self._create_filename()
        new = open(os.path.join(settings.MEDIA_ROOT, RESOURCES_DIRECTORY, filename), "w")
        new.write(text)
        new.close()

        try:
            old_filename = os.path.join(settings.MEDIA_ROOT, self.filename)
            os.unlink(old_filename)
        except OSError:
            pass

        self.last_updated = datetime.datetime.now()
        self.filename = filename
        self.position = position
        self.save()

        cache.set("resourcesmanager-%s" % self.type, self)

    def _create_filename(self):
        suffix = "css" if self.type == CSS else "js"
        if self.group:
            return "%s_%s.%s" % (self.group, datetime.datetime.now().strftime("%Y%m%d%H%M%S"), suffix)
        else:
            return "%s.%s" % (datetime.datetime.now().strftime("%Y%m%d%H%M%S"), suffix)

class Resource(models.Model):
    """A registered resource like CSS or Javascript.

    **Attributes**:

    path
        The path to the resource (without MEDIA_URL).

    position
        The position of the resource within the merged file (important if one
        resource is dependend of another).

    type
        The type of the resource: At the time being: Javascript or CSS.

    minify
        If True the resource is minified.

    media
        The media type of the resource. Only used for CSS resources.

    """
    path = models.CharField(_(u"Script"), max_length=255)
    position = models.PositiveIntegerField(default=10)
    type = models.PositiveSmallIntegerField(choices=RESOURCE_CHOICES)
    merge = models.PositiveSmallIntegerField(default=1)
    minify = models.PositiveSmallIntegerField(default=1)
    group = models.CharField(_(u"Group"), blank=True, max_length=255)
    media = models.CharField(blank=True, max_length=30)

    def __unicode__(self):
        return self.path

    class Meta:
        ordering = ("position", )
        
    def save(self, force_insert=False, force_update=False):
        """
        """
        super(Resource, self).save(force_insert, force_update)
        import resources.utils
        resources.utils.reset()
        resources.utils.create_resources()
        
    def get_path(self):
        """Returns the full path to the resource.
        """
        return os.path.join(RESOURCES_DIRECTORY, self.path)

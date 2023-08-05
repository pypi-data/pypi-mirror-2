"""Models for emencia.django.downloader"""
import random
from datetime import datetime
try:
    from hashlib import md5
except ImportError:
    #Python 2.4 support
    from md5 import new as md5

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Download(models.Model):
    """
    Download model
    """

    file = models.FileField(_('file'), upload_to='private')
    password = models.CharField(_('password'), max_length=50, blank=True)
    slug = models.SlugField(_('slug'), help_text=_('Used for the URLs'))
    creation = models.DateTimeField(_('creation date'), auto_now_add=True)
    last_download = models.DateTimeField(_('last download'), blank=True, null=True)

    def __unicode__(self):
        return self.file.url

    class Meta:
        verbose_name = _('download')
        verbose_name_plural = _('downloads')
        ordering = ('file',)

    def filename(self):
        return self.file.name.split('/')[-1]

    def save(self, *args, **kwargs):
        if self.slug == '':
            name = "%s%s%i" % (self.file.url, datetime.utcnow(), random.randint(0, 100000))
            self.slug = md5(name).hexdigest()

        super(Download, self).save(*args, **kwargs)

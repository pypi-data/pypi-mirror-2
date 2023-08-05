"""Admin for emencia.django.downloader"""
from django.contrib import admin
from django.utils.translation import ugettext as _

from emencia.django.downloader.models import Download

class DownloadAdmin(admin.ModelAdmin):
    list_display = ('filename', 'slug', 'creation')

admin.site.register(Download, DownloadAdmin)

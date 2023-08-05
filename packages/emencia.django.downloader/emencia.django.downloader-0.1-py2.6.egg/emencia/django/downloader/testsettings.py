"""Test setting for emencia.django.emencia.django.downloader"""
import os

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/emencia.django.downloader.db'
INSTALLED_APPS = ['emencia.django.downloader',]

ROOT_URLCONF = 'emencia.django.downloader.urls'

MEDIA_ROOT = 'tests'

LANGUAGE_CODE = 'en'

LANGUAGES = (
            ('fr', 'French'),
            ('en', 'English'),
                )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',)

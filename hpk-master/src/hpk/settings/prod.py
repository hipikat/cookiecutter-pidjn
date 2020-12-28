"""
Django settings for production
"""

from os import environ

from .base import *    # noqa


DJANGO_SECRET_KEY = environ.get('DJANGO_SECRET_KEY')

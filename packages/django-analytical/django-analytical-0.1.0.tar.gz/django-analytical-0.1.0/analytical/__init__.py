"""
Analytics service integration for Django
========================================

The django-analytical application integrates analytics services into a
Django_ project.  See the ``docs`` directory for more information.

.. _Django: http://www.djangoproject.com/
"""

__author__ = "Joost Cassee"
__email__ = "joost@cassee.net"
__version__ = "0.1.0"
__copyright__ = "Copyright (C) 2011 Joost Cassee"
__license__ = "MIT License"

try:
    from collections import namedtuple
except ImportError:
    namedtuple = lambda name, fields: lambda *values: values

Property = namedtuple('Property', ['num', 'name', 'value'])

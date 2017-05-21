"""
Production settings.
"""

from fitjeb.settings.base import *


# Turn off debug during production
DEBUG = False

# Be more selective about hosts
ALLOWED_HOSTS = ['.elasticbeanstalk.com']


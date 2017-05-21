from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import os.environ as env

class Command(BaseCommand):

    def handle(self, *args, **options):
        if 'ADMIN_USERNAME' in env and 'ADMIN_PASSWORD' in env and 'ADMIN_EMAIL' in env:
            if not User.objects.filter(username=env['ADMIN_USERNAME']).exists():
                User.objects.create_superuser(env['ADMIN_USERNAME'], env['ADMIN_PASSWORD'], env['ADMIN_EMAIL'])

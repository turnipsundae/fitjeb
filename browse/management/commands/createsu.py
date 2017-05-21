from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        if 'ADMIN_USERNAME' in os.environ and 'ADMIN_PASSWORD' in os.environ and 'ADMIN_EMAIL' in os.environ:
            if not User.objects.filter(username=os.environ['ADMIN_USERNAME']).exists():
                User.objects.create_superuser(os.environ['ADMIN_USERNAME'], os.environ['ADMIN_PASSWORD'], os.environ['ADMIN_EMAIL'])

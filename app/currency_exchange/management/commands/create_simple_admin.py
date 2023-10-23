from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Creating Admin...')
        if User.objects.filter(username='admin', is_superuser=True, is_staff=True).exists():
            self.stdout.write(self.style.SUCCESS('Admin alredy exist!'))
        else:
            user = User.objects.create_user('admin', password='admin')
            user.is_superuser = True
            user.is_staff = True
            user.save()

            self.stdout.write(self.style.SUCCESS('Admin has been created!'))

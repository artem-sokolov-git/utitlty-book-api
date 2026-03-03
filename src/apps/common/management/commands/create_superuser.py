from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create superuser from settings (ADMIN_USER, ADMIN_PASSWORD)"

    def handle(self, *args, **options):
        username = settings.ADMIN_USER
        password = settings.ADMIN_PASSWORD

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists."))
            return

        User.objects.create_superuser(username=username, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully."))

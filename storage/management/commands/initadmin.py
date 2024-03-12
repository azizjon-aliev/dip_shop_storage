from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        USERNAME = 'admin'
        PASSWORD = 'admin'
        

        if not User.objects.filter(username=USERNAME).exists():
            print("Creating admin account...")
            User.objects.create_superuser(
                username=USERNAME, password=PASSWORD
            )
        else:
            print("Admin already initialized...")
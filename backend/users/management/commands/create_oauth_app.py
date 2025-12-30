from django.core.management.base import BaseCommand
from oauth2_provider.models import Application
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import secrets

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates OAuth2 application for frontend if it does not exist'

    def handle(self, *args, **kwargs):
        # Check if application already exists
        if Application.objects.filter(name="Skriptomat Frontend").exists():
            self.stdout.write(self.style.SUCCESS('OAuth2 application "Skriptomat Frontend" already exists'))
            return

        # Get or create a superuser for the application
        # In production, this should be a proper admin user
        # For now, we'll use the first superuser or create a system user
        admin_user = User.objects.filter(is_superuser=True).first()
        
        if not admin_user:
            # Create a system user for OAuth app ownership
            random_password = secrets.token_urlsafe(32)
            admin_user = User.objects.create_superuser(
                username='oauth_admin',
                email='admin@skriptomat.local',
                password=random_password
            )
            self.stdout.write(self.style.WARNING('Created system admin user for OAuth application'))

        # Create the OAuth2 application
        app = Application.objects.create(
            name="Skriptomat Frontend",
            user=admin_user,
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD,
            skip_authorization=True,
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created OAuth2 application: {app.name}'))
        self.stdout.write(self.style.SUCCESS(f'Client ID: {app.client_id}'))

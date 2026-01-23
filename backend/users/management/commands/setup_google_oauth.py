from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
import os


class Command(BaseCommand):
    help = 'Setup Google OAuth for django-allauth'

    def handle(self, *args, **kwargs):
        # Get Google credentials from environment
        client_id = os.environ.get('GOOGLE_CLIENT_ID')
        # Note: Client secret is not needed for frontend-only OAuth flow
        # but allauth requires it - use a placeholder or get from env
        client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', 'not-needed-for-frontend-flow')
        
        if not client_id:
            self.stdout.write(self.style.ERROR('GOOGLE_CLIENT_ID not found in environment variables!'))
            return

        # Update or create Site
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': 'skriptomat-fork.vercel.app',
                'name': 'Skriptomat'
            }
        )
        
        if not created:
            site.domain = 'skriptomat-fork.vercel.app'
            site.name = 'Skriptomat'
            site.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Updated Site: {site.domain}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✓ Created Site: {site.domain}'))

        # Create or update Google OAuth app
        app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': client_id,
                'secret': client_secret
            }
        )
        
        if not created:
            app.name = 'Google'
            app.client_id = client_id
            app.secret = client_secret
            app.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Updated Google OAuth app'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✓ Created Google OAuth app'))
        
        # Associate with site
        if site not in app.sites.all():
            app.sites.add(site)
            self.stdout.write(self.style.SUCCESS(f'✓ Associated Google app with site'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Google OAuth setup complete!'))

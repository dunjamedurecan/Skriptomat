from django.core.management.base import BaseCommand
from users.models import Role


class Command(BaseCommand):
    help = 'Create default roles (student, moderator, admin)'

    def handle(self, *args, **kwargs):
        roles = [
            Role.STUDENT,
            Role.MODERATOR,
            Role.ADMIN,
        ]

        for role_name in roles:
            role, created = Role.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Created role: {role_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  Role already exists: {role_name}'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Roles seeded successfully!'))

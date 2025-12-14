"""
Management command to seed baseline users and teams.

Creates:
- Superuser: admin@example.com / admin1234
- User: joe@example.com / admin1234
- Teams: Team One, Team Two, Team Three (owned by Joe and with Joe as a member)
"""

# Django Imports
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

# First-Party Imports
from gc_users.models import Team


class Command(BaseCommand):
    help = "Seed baseline users and teams."

    def handle(self, *args, **options):
        User = get_user_model()

        # Create or update superuser
        admin_user, created_admin = User.objects.get_or_create(
            email="admin@example.com",
            defaults={"is_staff": True, "is_superuser": True},
        )
        if created_admin:
            admin_user.set_password("admin1234")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created superuser admin@example.com"))
        else:
            # Ensure privileges in case record was modified
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.set_password("admin1234")
            admin_user.save()
            self.stdout.write(self.style.WARNING("Updated password/flags for admin@example.com"))

        # Create or update Joe
        joe_user, created_joe = User.objects.get_or_create(
            email="joe@example.com",
            defaults={"first_name": "Joe", "last_name": "Example"},
        )
        joe_user.set_password("admin1234")
        joe_user.save()
        if created_joe:
            self.stdout.write(self.style.SUCCESS("Created user joe@example.com"))
        else:
            self.stdout.write(self.style.WARNING("Updated password for joe@example.com"))

        # Create teams and attach Joe as owner/member
        team_names = ["Team One", "Team Two", "Team Three"]
        for name in team_names:
            team, created_team = Team.objects.get_or_create(name=name, defaults={"owner": joe_user})
            # If existing, ensure owner set to Joe (primary contact intent)
            if team.owner != joe_user:
                team.owner = joe_user
            team.save()
            team.users.add(joe_user)

            status = "Created" if created_team else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{status} team '{name}' with Joe as owner/member"))

        self.stdout.write(self.style.SUCCESS("User and team seeding complete."))

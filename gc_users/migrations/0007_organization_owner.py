# Generated manually because automatic makemigrations isn't available in this environment.

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gc_users", "0006_organization_users"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                help_text="User who owns this organization.",
                null=True,
                on_delete=models.SET_NULL,
                related_name="owned_organizations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

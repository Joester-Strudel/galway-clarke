# Generated manually because the environment for makemigrations was unavailable.

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gc_users", "0005_remove_apikey_created_by_remove_apikey_routes_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="users",
            field=models.ManyToManyField(
                blank=True,
                help_text="Users who belong to this organization.",
                related_name="organizations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

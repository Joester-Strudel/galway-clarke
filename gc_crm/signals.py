# Django Imports
from django.db.models.signals import post_save
from django.dispatch import receiver

# First-Party Imports
from gc_crm.models import Industry, Status, Tag
from gc_users.models import Team


DEFAULT_STATUSES = [
    ("Active", "green"),
    ("Prospect", "sky"),
    ("Churned", "rose"),
]

DEFAULT_INDUSTRIES = [
    ("Museum", "blue"),
    ("Gallery", "violet"),
    ("Non-Profit", "emerald"),
]

DEFAULT_TAGS = [
    ("Major Donor", "rose"),
    ("Volunteer", "amber"),
    ("Event Lead", "indigo"),
]


def _ensure_default_definitions(team: Team) -> None:
    """Seed a handful of sensible defaults for a newly created team."""
    for name, color in DEFAULT_STATUSES:
        Status.objects.get_or_create(team=team, name=name, defaults={"color": color})

    for name, color in DEFAULT_INDUSTRIES:
        Industry.objects.get_or_create(team=team, name=name, defaults={"color": color})

    for name, color in DEFAULT_TAGS:
        Tag.objects.get_or_create(team=team, name=name, defaults={"color": color})


@receiver(post_save, sender=Team)
def create_team_defaults(sender, instance: Team, created: bool, **kwargs):
    """
    When a new team is created, populate a small set of default CRM definitions.
    """
    if not created:
        return
    _ensure_default_definitions(instance)

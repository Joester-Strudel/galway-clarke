"""
Helper to generate sample CRM organizations for development.
"""

# Standard Library Imports
import random
from datetime import timedelta

# Django Imports
from django.utils import timezone

# First-Party Imports
from gc_crm.models import Industry, Organization, Status
from gc_users.models import Team, GcUser


def seed_organizations():
    """
    Create 50 sample organizations tied to Team One (owned by joe@example.com).
    Safe to re-run; will not duplicate names.
    """
    team = Team.objects.filter(name="Team One").first()
    joe = GcUser.objects.filter(email="joe@example.com").first()

    if not team:
        print("Team One not found; aborting organization seed.")
        return
    if joe and not team.owner:
        team.owner = joe
        team.save()
    if joe:
        team.users.add(joe)

    # Ensure a couple of statuses/industries exist
    default_status, _ = Status.objects.get_or_create(name="Active", defaults={"team": team})
    pending_status, _ = Status.objects.get_or_create(name="Prospect", defaults={"team": team})
    museum_industry, _ = Industry.objects.get_or_create(name="Museum", defaults={"team": team})
    gallery_industry, _ = Industry.objects.get_or_create(name="Gallery", defaults={"team": team})

    sample_names = [
        "Acme Arts Museum",
        "Harbor City Gallery",
        "Greenwood Cultural Center",
        "Riverfront Arts Alliance",
        "Bayview Maritime Museum",
        "Sunrise History Center",
        "Prairie Heritage Trust",
        "Harborview Arts Collective",
        "Crescent City Arts",
        "Summit Arts Council",
        "Evergreen Creative Hub",
        "Lighthouse Cultural Center",
        "Meadowbrook Arts Guild",
        "Silverline Gallery",
        "Foundry Arts Studio",
        "Cobalt Arts House",
        "Elmwood Arts League",
        "Hillcrest Museum",
        "Mariner Arts Center",
        "Seaside Gallery",
        "Oak & Stone Museum",
        "Heritage Row Collective",
        "Sundial Arts",
        "Cedar Grove Museum",
        "Vista Arts Hub",
        "Civic Arts Forum",
        "Canyon Ridge Museum",
        "Granite Gallery",
        "Riverside Arts Network",
        "Aspen Arts Foundation",
        "Northstar Museum",
        "Juniper Arts Center",
        "Wildflower Gallery",
        "Blue Harbor Arts",
        "Maple Crest Museum",
        "Broadway Arts Co-Op",
        "Harbor Lights Arts",
        "Timberline Cultural Center",
        "Horizon Arts League",
        "Pioneer Heritage Center",
        "Garden City Gallery",
        "Harpswell Arts Guild",
        "Crown Point Museum",
        "Cascadia Arts",
        "Driftwood Arts Society",
        "Lakeshore Gallery",
        "Bridgeview Arts",
        "Union Arts Cooperative",
        "Copperleaf Cultural Center",
        "Starlight Arts Studio",
    ]

    created_count = 0
    for name in sample_names:
        org, created = Organization.objects.get_or_create(
            team=team,
            name=name,
            defaults={
                "status": default_status,
                "industry": random.choice([museum_industry, gallery_industry]),
                "last_activity_at": timezone.now() - timedelta(days=random.randint(0, 60)),
                "notes": "Sample organization record for development.",
            },
        )
        if created:
            created_count += 1
        else:
            # Refresh a couple fields for variety
            org.status = random.choice([default_status, pending_status])
            org.industry = random.choice([museum_industry, gallery_industry])
            org.last_activity_at = timezone.now() - timedelta(days=random.randint(0, 60))
            org.save()

    print(f"Seeded {created_count} organizations (upserted {len(sample_names)}).")

# Standard Library Imports
# Standard Library Imports
import os
from urllib.parse import urlsplit

# Django Imports
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client

# First-Party Imports
from gc_geography.models import City, County, State, ZipCode
from gc_users.models import Team
from gc_crm.models import Organization, Status

# Allow Django ORM usage in async-capable test runner contexts (Playwright).
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

@pytest.fixture
def user_and_team(db):
    """
    Create a user and a team; the gc_crm signals will seed default statuses/industries/tags.
    """
    User = get_user_model()
    user = User.objects.create_user(
        email="playwright@example.com",
        password="testpass123",
        first_name="Play",
        last_name="Wright",
    )
    team = Team.objects.create(name="Playwright Team", owner=user)
    team.users.add(user)
    # Ensure a baseline organization exists for edit flows
    default_status = Status.objects.filter(team=team).first()
    Organization.objects.create(
        team=team,
        name="Seed Organization",
        status=default_status,
        notes="Seeded for E2E tests.",
    )
    return user, team


@pytest.fixture
def geo_seed(db):
    """
    Seed minimal geography data so remote selects have values to pick.
    """
    ohio, _ = State.objects.get_or_create(name="Ohio", abbreviation="OH")
    cuyahoga, _ = County.objects.get_or_create(name="Cuyahoga", state=ohio)
    rocky_river, _ = City.objects.get_or_create(name="Rocky River", state=ohio, county=cuyahoga)
    zip_obj, _ = ZipCode.objects.get_or_create(zip_code_five_digit="44116")
    zip_obj.states.add(ohio)
    zip_obj.counties.add(cuyahoga)
    zip_obj.cities.add(rocky_river)
    return {"state": ohio, "county": cuyahoga, "city": rocky_river, "zip": zip_obj}


@pytest.fixture
def auth_page(page, live_server, user_and_team):
    """
    Log the Playwright page in by copying a Django session cookie from the test client.
    """
    user, _team = user_and_team
    client = Client()
    logged_in = client.login(email=user.email, password="testpass123")
    assert logged_in, "Failed to log in test user"

    # Set the active organization to bypass the select-organization screen.
    session = client.session
    session["active_organization_id"] = str(_team.id)
    session.save()

    session_cookie = client.cookies.get(settings.SESSION_COOKIE_NAME)
    assert session_cookie, "No session cookie found after login"

    server_url = live_server.url  # e.g., http://localhost:8081
    parsed = urlsplit(server_url)
    domain = parsed.hostname

    page.context.add_cookies(
        [
            {
                "name": settings.SESSION_COOKIE_NAME,
                "value": session_cookie.value,
                "domain": domain,
                "path": "/",
                "httpOnly": False,
                "secure": False,
            }
        ]
    )
    return page

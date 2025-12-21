# Standard Library Imports
import os

# Django Imports
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client

# First-Party Imports
from gc_users.models import Team

# Allow ORM in async-capable Playwright runner
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def user_and_team(db):
    """
    Create a baseline user and team for auth flows.
    """
    User = get_user_model()
    user = User.objects.create_user(
        email="users-e2e@example.com",
        password="testpass123",
        first_name="User",
        last_name="E2E",
    )
    team = Team.objects.create(name="Users E2E Team", owner=user)
    team.users.add(user)
    return user, team


@pytest.fixture
def auth_page(page, live_server, user_and_team):
    """
    Log the Playwright page in by copying a Django session cookie; set active org.
    """
    user, team = user_and_team
    client = Client()
    logged_in = client.login(email=user.email, password="testpass123")
    assert logged_in, "Failed to log in test user"

    session = client.session
    session["active_organization_id"] = str(team.id)
    session.save()

    session_cookie = client.cookies.get(settings.SESSION_COOKIE_NAME)
    assert session_cookie, "No session cookie found after login"

    parsed = live_server.url.split("//", 1)[-1]
    domain = parsed.split(":")[0]

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

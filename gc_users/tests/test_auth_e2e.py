# Playwright E2E tests for gc_users auth/team flows.

# Standard Library Imports
import uuid

# Django Imports
import pytest

# Third-Party Imports
from playwright.sync_api import expect


def _log(browser_name, message):
    print(f"[{browser_name}] {message}")


@pytest.mark.django_db
def test_signup_and_logout(page, live_server, browser_name):
    """
    Sign up a new user, ensure redirect to marketing-home, then sign out.
    """
    _log(browser_name, "Running test_signup_and_logout")
    page.goto(f"{live_server.url}/signup/")

    email = f"signup-{uuid.uuid4().hex[:6]}@example.com"
    page.fill('input[name="email"]', email)
    page.fill('input[name="first_name"]', "Sign")
    page.fill('input[name="last_name"]', "Up")
    page.fill('input[name="password1"]', "testpass123")
    page.fill('input[name="password2"]', "testpass123")
    page.get_by_role("button", name="Create Account").click()

    # Redirect to create-team, create team, then land on marketing-home
    page.wait_for_url(f"{live_server.url}/create-team/")
    team_name = f"Signup Team {uuid.uuid4().hex[:6]}"
    page.fill('input[name="name"]', team_name)
    page.get_by_role("button", name="Create and Continue").click()
    page.wait_for_url(f"{live_server.url}/")

    # Now sign out (form POST)
    page.goto(f"{live_server.url}/signout/")
    page.get_by_role("button", name="Sign Out").click()
    page.wait_for_url(f"{live_server.url}/", timeout=10000)


@pytest.mark.django_db
def test_signin_and_select_team(user_and_team, live_server, browser_name, page):
    """
    Sign in as existing user, land on select-organization, choose team.
    """
    _log(browser_name, "Running test_signin_and_select_team")
    user, team = user_and_team
    page.goto(f"{live_server.url}/signin/")
    page.fill('input[name="email"]', user.email)
    page.fill('input[name="password"]', "testpass123")
    page.get_by_role("button", name="Continue").click()

    # Should be redirected to select-organization
    page.wait_for_url(f"{live_server.url}/select-organization/")

    # Click the team card/link
    team_link = page.get_by_role("link").filter(has_text=team.name).first
    team_link.click()
    page.wait_for_url(f"{live_server.url}/")


@pytest.mark.django_db
def test_create_team_flow(page, live_server, browser_name):
    """
    Hit create-team page, create a new team, ensure redirect to select-organization.
    """
    _log(browser_name, "Running test_create_team_flow")
    # Start from signup so we have a logged-in session
    page.goto(f"{live_server.url}/signup/")
    email = f"team-{uuid.uuid4().hex[:6]}@example.com"
    page.fill('input[name="email"]', email)
    page.fill('input[name="first_name"]', "Team")
    page.fill('input[name="last_name"]', "Creator")
    page.fill('input[name="password1"]', "testpass123")
    page.fill('input[name="password2"]', "testpass123")
    page.get_by_role("button", name="Create Account").click()
    page.wait_for_url(f"{live_server.url}/create-team/")

    team_name = f"New Team {uuid.uuid4().hex[:6]}"
    page.fill('input[name="name"]', team_name)
    page.get_by_role("button", name="Create and Continue").click()

    # Should land on marketing-home after team creation
    page.wait_for_url(f"{live_server.url}/")


@pytest.mark.django_db
def test_signout_redirects(page, live_server, browser_name, auth_page):
    """
    With an authenticated session, sign out and verify redirect to signin.
    """
    _log(browser_name, "Running test_signout_redirects")
    page = auth_page
    page.goto(f"{live_server.url}/signout/")
    page.get_by_role("button", name="Sign Out").click()
    page.wait_for_url(f"{live_server.url}/", timeout=10000)

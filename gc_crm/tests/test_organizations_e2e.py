# Pytest + Playwright E2E coverage for core CRM flows.

# Standard Library Imports
import uuid

# Django Imports
import pytest

# Third-Party Imports
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

# First-Party Imports
from gc_crm.models import Organization, Status, Tag

ORGS_PATH = "/crm/organizations/"


def _log(browser_name, message):
    print(f"[{browser_name}] {message}")


def _open_first_org_drawer(page):
    """
    Click the first "open drawer" button in the organizations table and wait for the drawer to render.
    """
    page.wait_for_selector("#crm_table_content tbody tr")
    page.locator('tbody tr button[hx-get*="/crm/organizations/"][hx-swap="outerHTML"]').first.click()
    page.wait_for_selector("#organization_drawer_content form")


def _open_org_by_name(page, name):
    """
    Open the drawer for the row that contains the given organization name.
    """
    row = page.locator("tr", has_text=name).first
    row.locator('button[hx-get*="/crm/organizations/"][hx-swap="outerHTML"]').click()
    page.wait_for_selector("#organization_drawer_content form")


def _select_remote_option(page, button_selector, option_text, ensure_present=True):
    """
    Open a remote pill select, choose an option, and close the dropdown.
    If ensure_present is False, wait for the pill to disappear (used to unselect).
    """
    dropdown = page.locator(button_selector).first
    dropdown.click()
    try:
        # Scope to this dropdown's options container if possible
        btn_id = dropdown.get_attribute("id")
        options_container = f"#{btn_id}_options" if btn_id else "[data-options-container]"
        container_locator = page.locator(options_container).first
        try:
            container_locator.wait_for(state="visible", timeout=4000)
        except PlaywrightTimeoutError:
            # Try re-opening the dropdown once if the container is still hidden
            dropdown.click()
            container_locator.wait_for(state="visible", timeout=4000)

        option = container_locator.locator("[data-value]").filter(has_text=option_text).first
        option.scroll_into_view_if_needed()
        option.click(force=True)
    except PlaywrightTimeoutError:
        # Re-raise to fail fast instead of clicking the wrong dropdown.
        raise
    # Wait for selection pill to appear inside the button (collapsed state)
    page.keyboard.press("Escape")
    locator = page.locator(f"{button_selector} span", has_text=option_text)
    if ensure_present:
        locator.first.wait_for(timeout=4000)
    else:
        locator.wait_for(state="hidden", timeout=4000)


def _delete_open_record(page):
    """
    From an open drawer, trigger delete confirmation and confirm deletion.
    """
    delete_btn = page.get_by_role("button", name="Delete")
    delete_btn.click()
    with page.expect_response(
        lambda r: "/organizations/" in r.url and "/delete/" in r.url and r.request.method == "POST",
        timeout=4000,
    ) as resp:
        page.get_by_role("button", name="Yes").click()
    response = resp.value
    assert response.status == 200


def _fill_notes(page, text):
    """
    Type into the WYSIWYG rich text field.
    """
    editor = page.locator('div[contenteditable="true"]').first
    editor.click()
    editor.fill(text)


def _fill_notes_formatted(page):
    """
    Add formatted content (bold, italic, underline, new paragraphs) to the rich text field.
    """
    drawer = page.locator("#organization_drawer_content")
    editor = drawer.locator('div[contenteditable="true"]').first
    bold_btn = drawer.get_by_role("button", name="Bold").first
    italic_btn = drawer.get_by_role("button", name="Italic").first
    underline_btn = drawer.get_by_role("button", name="Underline").first

    editor.click()
    bold_btn.click()
    page.keyboard.type("Bold line")
    page.keyboard.press("Enter")

    italic_btn.click()
    page.keyboard.type("Italic line")
    page.keyboard.press("Enter")

    underline_btn.click()
    page.keyboard.type("Underlined line")
    page.keyboard.press("Enter")

    page.keyboard.type("Plain paragraph after formatting.")


def _close_drawer(page):
    """
    Click the drawer overlay to close it (no-op if already closed).
    """
    overlay = page.locator("div.bg-black\\/50").last
    try:
        if overlay.count():
            overlay.click(force=True)
            overlay.wait_for(state="hidden", timeout=3000)
        else:
            # Fallback: click near top-left outside the drawer
            page.mouse.click(5, 5)
    except Exception:
        page.mouse.click(5, 5)


def _click_save_and_wait(page, match_fn):
    """
    Click the Save button and wait for the matching POST response (htmx swap).
    """
    with page.expect_response(match_fn, timeout=4000) as resp:
        page.get_by_role("button", name="Save").click()
    response = resp.value
    assert response.status == 200, f"Unexpected status: {response.status}"
    page.wait_for_selector("#organization_drawer_content form")


@pytest.mark.django_db
def test_open_drawer_and_edit(auth_page, live_server, geo_seed, browser_name):
    _log(browser_name, "Running test_open_drawer_and_edit")
    page = auth_page
    page.goto(f"{live_server.url}{ORGS_PATH}")

    _open_first_org_drawer(page)

    new_name = f"Updated Org {uuid.uuid4().hex[:6]}"
    page.fill('input[name="name"]', new_name)

    # Remote select: choose a status (default seeded by signal)
    _select_remote_option(page, 'button[id^="org_status_"]', "Active")
    _select_remote_option(page, 'button[id^="org_industry_"]', "Museum")
    _select_remote_option(page, 'button[id^="org_tags_"]', "Major Donor")
    _select_remote_option(page, 'button[id^="org_tags_"]', "Volunteer")

    # Address tab: fill address fields and select geo lookups
    page.get_by_role("button", name="Address").click()
    page.fill('input[name="address_one"]', "1234 Main St.")
    page.fill('input[name="address_two"]', "APT 2")
    _select_remote_option(page, 'button[id^="org_city_"]', "Rocky River")
    _select_remote_option(page, 'button[id^="org_county_"]', "Cuyahoga")
    _select_remote_option(page, 'button[id^="org_state_"]', "Ohio")
    _select_remote_option(page, 'button[id^="org_zip_"]', "44116")

    # Notes rich text (formatted)
    page.get_by_role("button", name="Notes").click()
    _fill_notes_formatted(page)

    _click_save_and_wait(
        page,
        lambda r: "/crm/organizations/" in r.url and "/edit/" in r.url and r.request.method == "POST",
    )
    page.wait_for_selector(f"text={new_name}", timeout=5000)
    assert page.get_by_text(new_name).first.is_visible()
    _close_drawer(page)


@pytest.mark.django_db
def test_create_new_org(auth_page, live_server, geo_seed, browser_name):
    _log(browser_name, "Running test_create_new_org")
    page = auth_page
    page.goto(f"{live_server.url}{ORGS_PATH}")

    # Click the default Add button in table_tools
    page.get_by_role("button", name="Add").click()
    page.wait_for_selector("#organization_drawer_content form")

    new_name = f"New Org {uuid.uuid4().hex[:6]}"
    page.fill('input[name="name"]', new_name)
    _select_remote_option(page, 'button[id^="org_status_"]', "Active")
    _select_remote_option(page, 'button[id^="org_industry_"]', "Museum")
    _select_remote_option(page, 'button[id^="org_tags_"]', "Major Donor")
    _select_remote_option(page, 'button[id^="org_tags_"]', "Volunteer")
    page.get_by_role("button", name="Notes").click()
    _fill_notes_formatted(page)

    _click_save_and_wait(
        page,
        lambda r: "/crm/organizations/" in r.url and "/new/" in r.url and r.request.method == "POST",
    )
    page.wait_for_selector(f"text={new_name}", timeout=5000)
    assert page.get_by_text(new_name).first.is_visible()
    _close_drawer(page)


@pytest.mark.django_db
def test_tab_persists_on_save(auth_page, live_server, geo_seed, browser_name):
    """
    Switch to Address tab, save, and confirm the tab stays selected after reload.
    """
    _log(browser_name, "Running test_tab_persists_on_save")
    page = auth_page
    page.goto(f"{live_server.url}{ORGS_PATH}")
    _open_first_org_drawer(page)

    # Go to Address tab and add a small tweak
    page.get_by_role("button", name="Address").click()
    page.fill('input[name="address_one"]', "123 Test St")
    _click_save_and_wait(
        page,
        lambda r: "/crm/organizations/" in r.url and "/edit/" in r.url and r.request.method == "POST",
    )

    # After HTMX swap, the Address tab should still be active
    page.wait_for_selector("#organization_drawer_content form")
    active_address = page.get_by_role("button", name="Address")
    assert "border-gc-theme-accent" in active_address.get_attribute("class")

@pytest.mark.django_db
def test_delete_record(auth_page, live_server, geo_seed, browser_name):
    """
    Create a record and then delete it, verifying it disappears from the table.
    """
    _log(browser_name, "Running test_delete_record")
    page = auth_page
    page.goto(f"{live_server.url}{ORGS_PATH}")

    # Create a fresh record
    page.get_by_role("button", name="Add").click()
    page.wait_for_selector("#organization_drawer_content form")
    base_name = f"Delete Org {uuid.uuid4().hex[:6]}"
    page.fill('input[name="name"]', base_name)
    _select_remote_option(page, 'button[id^="org_status_"]', "Active")
    _select_remote_option(page, 'button[id^="org_industry_"]', "Museum")
    _click_save_and_wait(
        page,
        lambda r: "/crm/organizations/" in r.url and "/new/" in r.url and r.request.method == "POST",
    )
    page.wait_for_selector(f"text={base_name}", timeout=5000)
    _close_drawer(page)

    # Reopen and delete
    _open_org_by_name(page, base_name)
    _delete_open_record(page)
    page.wait_for_selector(f"text={base_name}", state="hidden", timeout=5000)
    page.wait_for_timeout(3000)


@pytest.mark.django_db
def test_edit_created_record(auth_page, live_server, geo_seed, browser_name):
    """
    Create a new record, then reopen it and edit each field before saving.
    """
    _log(browser_name, "Running test_edit_created_record")
    page = auth_page
    page.goto(f"{live_server.url}{ORGS_PATH}")

    # Create a fresh record
    page.get_by_role("button", name="Add").click()
    page.wait_for_selector("#organization_drawer_content form")

    base_name = f"E2E Org {uuid.uuid4().hex[:6]}"
    page.fill('input[name="name"]', base_name)
    _select_remote_option(page, 'button[id^="org_status_"]', "Active")
    _select_remote_option(page, 'button[id^="org_industry_"]', "Museum")
    _select_remote_option(page, 'button[id^="org_tags_"]', "Major Donor")
    _select_remote_option(page, 'button[id^="org_tags_"]', "Volunteer")
    page.get_by_role("button", name="Address").click()
    page.fill('input[name="address_one"]', "1234 Main St.")
    page.fill('input[name="address_two"]', "APT 2")
    _select_remote_option(page, 'button[id^="org_city_"]', "Rocky River")
    _select_remote_option(page, 'button[id^="org_county_"]', "Cuyahoga")
    _select_remote_option(page, 'button[id^="org_state_"]', "Ohio")
    _select_remote_option(page, 'button[id^="org_zip_"]', "44116")
    page.get_by_role("button", name="Notes").click()
    _fill_notes_formatted(page)
    _click_save_and_wait(
        page,
        lambda r: "/crm/organizations/" in r.url and "/new/" in r.url and r.request.method == "POST",
    )
    page.wait_for_selector(f"text={base_name}", timeout=5000)
    _close_drawer(page)

    # Reopen the newly created record and edit fields
    _open_org_by_name(page, base_name)
    edited_name = f"{base_name} Edited"
    page.fill('input[name="name"]', edited_name)
    _select_remote_option(page, 'button[id^="org_status_"]', "Prospect")
    _select_remote_option(page, 'button[id^="org_industry_"]', "Gallery")
    # Toggle a tag off/on to change selection
    _select_remote_option(page, 'button[id^="org_tags_"]', "Volunteer", ensure_present=False)  # removes
    _select_remote_option(page, 'button[id^="org_tags_"]', "Event Lead")  # adds

    page.get_by_role("button", name="Address").click()
    page.fill('input[name="address_one"]', "999 New Rd")
    page.fill('input[name="address_two"]', "Suite 10")
    _select_remote_option(page, 'button[id^="org_city_"]', "Rocky River")
    _select_remote_option(page, 'button[id^="org_county_"]', "Cuyahoga")
    _select_remote_option(page, 'button[id^="org_state_"]', "Ohio")
    _select_remote_option(page, 'button[id^="org_zip_"]', "44116")

    page.get_by_role("button", name="Notes").click()
    editor = page.locator("#organization_drawer_content div[contenteditable='true']").first
    editor.click()
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    _fill_notes_formatted(page)

    _click_save_and_wait(
        page,
        lambda r: "/crm/organizations/" in r.url and "/edit/" in r.url and r.request.method == "POST",
    )
    page.wait_for_selector(f"text={edited_name}", timeout=5000)
    _close_drawer(page)


@pytest.mark.django_db
def test_search_and_filter(auth_page, live_server, user_and_team, browser_name):
    """
    Verify search narrows results and filters can combine status + tag constraints.
    """
    _log(browser_name, "Running test_search_and_filter")
    page = auth_page
    _, team = user_and_team

    active_status = Status.objects.filter(team=team, name="Active").first()
    prospect_status = Status.objects.filter(team=team, name="Prospect").first()
    volunteer_tag = Tag.objects.filter(team=team, name="Volunteer").first()
    donor_tag = Tag.objects.filter(team=team, name="Major Donor").first()
    assert active_status and prospect_status and volunteer_tag and donor_tag

    # Seed a few organizations with different attributes to exercise search + filters.
    search_target = Organization.objects.create(
        team=team,
        name="Searchable Alpha Org",
        status=active_status,
    )
    search_target.tags.add(volunteer_tag)
    filter_target = Organization.objects.create(
        team=team,
        name="Filtered Prospect Org",
        status=prospect_status,
    )
    filter_target.tags.add(volunteer_tag)
    background_org = Organization.objects.create(
        team=team,
        name="Background Org",
        status=active_status,
    )
    background_org.tags.add(donor_tag)

    page.goto(f"{live_server.url}{ORGS_PATH}")

    # Search by name should only show the matching record.
    search_input = page.locator("[data-table-search-input]").first
    search_input.fill("Searchable Alpha")
    with page.expect_response(
        lambda r: "/crm/organizations/" in r.url and "search=Searchable" in r.url,
        timeout=5000,
    ):
        search_input.press("Enter")
    page.wait_for_selector("text=Searchable Alpha Org", timeout=5000)
    assert page.locator("tbody tr", has_text="Searchable Alpha Org").count() >= 1
    assert page.locator("tbody tr", has_text="Filtered Prospect Org").count() == 0
    assert page.locator("tbody tr", has_text="Background Org").count() == 0

    # Clear search, then apply filters for status + tag to isolate a different record.
    page.get_by_role("button", name="Filters").click()
    with page.expect_response(
        lambda r: "/crm/organizations/" in r.url and r.request.method == "GET",
        timeout=5000,
    ):
        page.get_by_role("button", name="Clear").click()
    search_input.fill("")

    page.fill('input[name="filter_status"]', "Prospect")
    page.fill('input[name="filter_tag"]', "Volunteer")
    with page.expect_response(
        lambda r: "/crm/organizations/" in r.url
        and "filter_status=Prospect" in r.url
        and "filter_tag=Volunteer" in r.url,
        timeout=5000,
    ):
        page.get_by_role("button", name="Apply Filters").click()

    page.wait_for_selector("text=Filtered Prospect Org", timeout=5000)
    assert page.locator("tbody tr", has_text="Filtered Prospect Org").count() >= 1
    assert page.locator("tbody tr", has_text="Background Org").count() == 0
    assert page.locator("tbody tr", has_text="Searchable Alpha Org").count() == 0

# Pytest + Playwright E2E coverage for CRM individuals workspace.

# Standard Library Imports
import uuid

# Django Imports
import pytest

# Third-Party Imports
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

INDIVIDUALS_PATH = "/crm/individuals/"


def _log(browser_name, message):
    print(f"[{browser_name}] {message}")


def _open_first_individual_drawer(page):
    """
    Click the first drawer button in the individuals table and wait for render.
    """
    page.wait_for_selector("#crm_table_content tbody tr")
    page.locator('tbody tr button[hx-get*="/crm/individuals/"][hx-swap="outerHTML"]').first.click()
    page.wait_for_selector("#individual_drawer_content form")


def _open_individual_by_name(page, name):
    """
    Open the drawer for the row that contains the given individual name.
    """
    row = page.locator("tr", has_text=name).first
    row.locator('button[hx-get*="/crm/individuals/"][hx-swap="outerHTML"]').click()
    page.wait_for_selector("#individual_drawer_content form")


def _select_remote_option(page, button_selector, option_text, ensure_present=True):
    """
    Open a remote pill select, choose an option, and close the dropdown.
    If ensure_present is False, wait for the pill to disappear (used to unselect).
    """
    dropdown = page.locator(button_selector).first
    dropdown.click()
    try:
        btn_id = dropdown.get_attribute("id")
        options_container = f"#{btn_id}_options" if btn_id else "[data-options-container]"
        container_locator = page.locator(options_container).first
        try:
            container_locator.wait_for(state="visible", timeout=4000)
        except PlaywrightTimeoutError:
            dropdown.click()
            container_locator.wait_for(state="visible", timeout=4000)

        option = container_locator.locator("[data-value]").filter(has_text=option_text).first
        option.scroll_into_view_if_needed()
        option.click(force=True)
    except PlaywrightTimeoutError:
        raise
    page.keyboard.press("Escape")
    # Ensure dropdown closes before interacting with other controls
    page.wait_for_timeout(200)
    locator = page.locator(f"{button_selector} span", has_text=option_text)
    if ensure_present:
        locator.first.wait_for(timeout=4000)
    else:
        # Wait for all matching pills to disappear when unselecting.
        page.wait_for_timeout(150)  # allow Alpine state to sync
        selector = f"{button_selector} span"
        page.wait_for_function(
            """([sel, text]) => {
              return [...document.querySelectorAll(sel)].filter(
                (el) => (el.textContent || '').trim() === text
              ).length === 0;
            }""",
            arg=[selector, option_text],
            timeout=4000,
        )


def _delete_open_record(page):
    """
    From an open drawer, trigger delete confirmation and confirm deletion.
    """
    delete_btn = page.get_by_role("button", name="Delete")
    delete_btn.click()
    with page.expect_response(
        lambda r: "/individuals/" in r.url and "/delete/" in r.url and r.request.method == "POST",
        timeout=4000,
    ) as resp:
        page.get_by_role("button", name="Yes").click()
    response = resp.value
    assert response.status == 200


def _fill_notes_formatted(page):
    """
    Add formatted content (bold, italic, underline, new paragraphs) to the rich text field.
    """
    drawer = page.locator("#individual_drawer_content")
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
    page.wait_for_selector("#individual_drawer_content form")


def _create_individual(page, name_seed):
    """
    Create a new individual via the Add drawer and return the display name used.
    """
    page.get_by_role("button", name="Add").click()
    page.wait_for_selector("#individual_drawer_content form")

    first_name = f"{name_seed} {uuid.uuid4().hex[:4]}"
    last_name = "Person"
    display_name = f"{first_name} {last_name}"
    page.fill('input[name="first_name"]', first_name)
    page.fill('input[name="last_name"]', last_name)
    page.fill('input[name="email"]', f"{uuid.uuid4().hex[:6]}@example.com")
    page.fill('input[name="phone"]', "5551239876")
    _select_remote_option(page, 'button[id^="individual_org_"]', "Seed Organization")
    _select_remote_option(page, 'button[id^="individual_tags_"]', "Major Donor")
    _select_remote_option(page, 'button[id^="individual_tags_"]', "Volunteer")
    page.get_by_label("Primary Contact").check()

    _click_save_and_wait(
        page,
        lambda r: "/crm/individuals/" in r.url and "/new/" in r.url and r.request.method == "POST",
    )
    page.wait_for_selector(f"text={display_name}", timeout=5000)
    _close_drawer(page)
    return display_name


@pytest.mark.django_db
def test_open_drawer_and_edit(auth_page, live_server, geo_seed, browser_name):
    _log(browser_name, "Running test_open_drawer_and_edit")
    page = auth_page
    page.goto(f"{live_server.url}{INDIVIDUALS_PATH}")

    _open_first_individual_drawer(page)

    first_name = f"Updated {uuid.uuid4().hex[:6]}"
    last_name = "Contact"
    page.fill('input[name="first_name"]', first_name)
    page.fill('input[name="last_name"]', last_name)
    page.fill('input[name="email"]', f"{uuid.uuid4().hex[:6]}@example.com")
    page.fill('input[name="phone"]', "5551112233")

    _select_remote_option(page, 'button[id^="individual_org_"]', "Seed Organization")
    _select_remote_option(page, 'button[id^="individual_tags_"]', "Major Donor")
    _select_remote_option(page, 'button[id^="individual_tags_"]', "Volunteer")
    page.get_by_label("Primary Contact").check()

    page.get_by_role("button", name="Address").click()
    page.fill('input[name="address_one"]', "1234 Main St.")
    page.fill('input[name="address_two"]', "APT 2")
    _select_remote_option(page, 'button[id^="individual_city_"]', "Rocky River")
    _select_remote_option(page, 'button[id^="individual_county_"]', "Cuyahoga")
    _select_remote_option(page, 'button[id^="individual_state_"]', "Ohio")
    _select_remote_option(page, 'button[id^="individual_zip_"]', "44116")

    page.get_by_role("button", name="Notes").click()
    _fill_notes_formatted(page)

    _click_save_and_wait(
        page,
        lambda r: "/crm/individuals/" in r.url and "/edit/" in r.url and r.request.method == "POST",
    )
    page.wait_for_selector(f"text={first_name} {last_name}", timeout=5000)
    _close_drawer(page)


@pytest.mark.django_db
def test_create_new_individual(auth_page, live_server, geo_seed, browser_name):
    _log(browser_name, "Running test_create_new_individual")
    page = auth_page
    page.goto(f"{live_server.url}{INDIVIDUALS_PATH}")

    new_name = _create_individual(page, "New Individual")
    page.wait_for_selector(f"text={new_name}", timeout=5000)
    _close_drawer(page)


@pytest.mark.django_db
def test_tab_persists_on_save(auth_page, live_server, geo_seed, browser_name):
    """
    Switch to Address tab, save, and confirm the tab stays selected after reload.
    """
    _log(browser_name, "Running test_tab_persists_on_save")
    page = auth_page
    page.goto(f"{live_server.url}{INDIVIDUALS_PATH}")
    _open_first_individual_drawer(page)

    page.get_by_role("button", name="Address").click()
    page.fill('input[name="address_one"]', "987 Persist Ave")
    _click_save_and_wait(
        page,
        lambda r: "/crm/individuals/" in r.url and "/edit/" in r.url and r.request.method == "POST",
    )

    page.wait_for_selector("#individual_drawer_content form")
    active_address = page.get_by_role("button", name="Address")
    assert "border-gc-theme-accent" in active_address.get_attribute("class")


@pytest.mark.django_db
def test_delete_record(auth_page, live_server, geo_seed, browser_name):
    """
    Create a record and then delete it, verifying it disappears from the table.
    """
    _log(browser_name, "Running test_delete_record")
    page = auth_page
    page.goto(f"{live_server.url}{INDIVIDUALS_PATH}")

    base_name = _create_individual(page, "Delete Individual")
    _open_individual_by_name(page, base_name)
    _delete_open_record(page)
    page.wait_for_selector(f"text={base_name}", state="hidden", timeout=5000)
    page.wait_for_timeout(2000)


@pytest.mark.django_db
def test_edit_created_record(auth_page, live_server, geo_seed, browser_name):
    """
    Create a new record, then reopen it and edit each field before saving.
    """
    _log(browser_name, "Running test_edit_created_record")
    page = auth_page
    page.goto(f"{live_server.url}{INDIVIDUALS_PATH}")

    base_name = _create_individual(page, "E2E Individual")
    _open_individual_by_name(page, base_name)

    edited_first = f"{base_name} Edited"
    edited_last = "Tester"
    page.fill('input[name="first_name"]', edited_first)
    page.fill('input[name="last_name"]', edited_last)
    page.fill('input[name="email"]', f"{uuid.uuid4().hex[:6]}@example.com")
    page.fill('input[name="phone"]', "5550001234")
    _select_remote_option(page, 'button[id^="individual_org_"]', "Seed Organization")
    _select_remote_option(page, 'button[id^="individual_tags_"]', "Volunteer", ensure_present=False)
    _select_remote_option(page, 'button[id^="individual_tags_"]', "Event Lead")
    page.get_by_label("Primary Contact").uncheck()

    page.get_by_role("button", name="Address").click()
    page.fill('input[name="address_one"]', "111 New Rd")
    page.fill('input[name="address_two"]', "Suite 10")
    _select_remote_option(page, 'button[id^="individual_city_"]', "Rocky River")
    _select_remote_option(page, 'button[id^="individual_county_"]', "Cuyahoga")
    _select_remote_option(page, 'button[id^="individual_state_"]', "Ohio")
    _select_remote_option(page, 'button[id^="individual_zip_"]', "44116")

    page.get_by_role("button", name="Notes").click()
    drawer = page.locator("#individual_drawer_content")
    editor = drawer.locator('div[contenteditable="true"]').first
    editor.click()
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    _fill_notes_formatted(page)

    _click_save_and_wait(
        page,
        lambda r: "/crm/individuals/" in r.url and "/edit/" in r.url and r.request.method == "POST",
    )
    page.wait_for_selector(f"text={edited_first} {edited_last}", timeout=5000)
    _close_drawer(page)

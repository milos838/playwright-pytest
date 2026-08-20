import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke
@pytest.mark.order("last")
def test_clear_test_data(page: Page, load_test_data):
    test_data = load_test_data
    page.goto(test_data["url"])
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    page.locator("#login-btn").click()
    page.locator("#nav-bookings").click()

    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Clear all bookings").click()

    expect(page.locator("#booking-card")).to_have_count(0)
    

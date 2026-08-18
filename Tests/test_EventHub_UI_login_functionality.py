import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke
def test_eventhub_ui_login_functionality(page: Page, load_test_data):
    test_data = load_test_data
    page.goto(test_data["url"])
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    page.locator("#login-btn").click()
    expect(page.locator("#user-email-display")).to_have_text(test_data["username"])
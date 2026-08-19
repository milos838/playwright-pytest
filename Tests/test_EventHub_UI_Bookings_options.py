import pytest
from playwright.sync_api import Page, expect

def test_eventhub_bookings_option1(page: Page, load_test_data):
    test_data = load_test_data
    page.goto(test_data["url"])
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    page.locator("#login-btn").click()
    page.locator("#nav-bookings").click()
    expect(page).to_have_url(test_data["bookings_url"])

def test_eventhub_bookings_option2(page: Page, load_test_data):
    test_data = load_test_data
    page.goto(test_data["url"])
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    page.locator("#login-btn").click()
    page.get_by_role("button", name="My Bookings").click()
    expect(page).to_have_url(test_data["bookings_url"])
    
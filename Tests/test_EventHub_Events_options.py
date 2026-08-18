import pytest
from playwright.sync_api import Page, expect

def test_eventhub_events_option(page: Page, load_test_data):
    test_data = load_test_data
    page.goto(test_data["url"])
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    page.locator("#login-btn").click()
    page.locator("#nav-events").click()
    expect(page).to_have_url(f"{test_data['events_url']}")

def test_eventhub_events_browseEvents(page: Page, load_test_data):
    test_data = load_test_data
    page.goto(test_data["url"])
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    page.locator("#login-btn").click()
    page.get_by_text("Browse Events →").click()
    expect(page).to_have_url(f"{test_data['events_url']}")

def test_eventhub_events_viewAll(page: Page, load_test_data):
    test_data = load_test_data
    page.goto(test_data["url"])
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    page.locator("#login-btn").click()
    page.get_by_text("View all →").click()
    expect(page).to_have_url(f"{test_data['events_url']}")







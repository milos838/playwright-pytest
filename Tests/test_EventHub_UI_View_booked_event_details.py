import pytest
from playwright.sync_api import Page, expect

def test_E2E_view_booked_event_details(page: Page, load_test_data):
    test_data = load_test_data
    page.goto(test_data["url"])
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    page.locator("#login-btn").click()
    page.locator("#nav-bookings").click()
    page.locator("#booking-card").first.get_by_role("button", name="View Details").click()
    expect(page.locator(".text-2xl")).to_contain_text(test_data["event_name"])
    page.locator("#check-refund-btn").click()
    expect(page.locator("#refund-result")).to_contain_text(test_data["refund_status"])



    
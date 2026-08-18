import pytest
from playwright.sync_api import Page, expect
from pytest_playwright.pytest_playwright import page

@pytest.mark.smoke
def test_E2E_book_an_event(page: Page, load_test_data):
    test_data = load_test_data
    page.goto(test_data["url"])
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    page.locator("#login-btn").click()
    page.locator('#book-now-btn[href="/events/2"]').click()
    page.locator("#customerName").fill(test_data["customer_name"])
    page.locator("#customer-email").fill(test_data["customer_email"])
    page.locator("#phone").fill(test_data["customer_phone"])
    page.locator("#confirm-booking").click()
    expect(page.locator(".text-xl")).to_contain_text("Booking Confirmed!")
   
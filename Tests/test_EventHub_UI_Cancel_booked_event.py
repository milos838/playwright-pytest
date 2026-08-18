import pytest
from playwright.sync_api import Page, expect

def test_E2E_cancel_booked_event(page: Page, load_test_data):
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
    page.locator("#nav-bookings").click()
    # waiting for the booking card to be visible before proceeding
    expect(page.locator("#booking-card").first).to_be_visible(timeout=15000)
    total_bookings = page.locator("#booking-card").count()
    print(f"Total bookings before cancellation: {total_bookings}")

    page.once("dialog", lambda dialog: dialog.accept())
    page.locator("#booking-card").last.locator("#cancel-booking-btn").click()
    page.get_by_role("button", name="Yes, cancel it").click()
    # waiting again for the booking card to be visible and validating count before proceeding
    expect(page.locator("#booking-card")).to_have_count(total_bookings - 1, timeout=15000)
    current_bookings = page.locator("#booking-card").count()
    print(f"Total bookings after cancellation: {current_bookings}")
    if current_bookings != total_bookings - 1:
        print("Booking cancellation failed. The booking card count did not decrease as expected.")
      
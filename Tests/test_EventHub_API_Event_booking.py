import pytest
from playwright.sync_api import Page, expect
from Utils.apiBase import APIutils


@pytest.mark.smoke
def test_book_event_through_api(page: Page, isolated_api_booking):
    token, booking_data = isolated_api_booking

    page.add_init_script(
        f"window.localStorage.setItem('eventhub_token', '{token}')"
    )

    page.goto(booking_data["url"])
    page.locator("#nav-bookings").click()
    booking_card = page.locator("#booking-card").filter(
        has_text=booking_data["customer_email"]
    )
    expect(booking_card.first).to_be_visible()
    
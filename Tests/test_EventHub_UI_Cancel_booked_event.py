import pytest
from playwright.sync_api import Page
from Pages.bookingsPage import BookingsPage
from Pages.eventPage import EventPage
from Pages.homePage import HomePage
from Pages.loginPage import LoginPage

def test_E2E_cancel_booked_event(page: Page, isolated_ui_booking):
    test_data = isolated_ui_booking
    home_page = HomePage(page)
    bookings_page = BookingsPage(page)

    home_page.navigate_to_bookings_from_header()
    bookings_page.wait_for_bookings()
    bookings_page.cancel_booking(test_data["booking_id"])
    assert bookings_page.booking_card_for(test_data["booking_id"]).count() == 0
      
import pytest
from playwright.sync_api import Page
from Pages.bookingsPage import BookingsPage
from Pages.eventPage import EventPage
from Pages.homePage import HomePage
from Pages.loginPage import LoginPage

def test_E2E_cancel_booked_event(page: Page, load_test_data):
    test_data = load_test_data
    login_page = LoginPage(page)
    event_page = EventPage(page)
    home_page = HomePage(page)
    bookings_page = BookingsPage(page)

    login_page.login(test_data)
    event_page.open_event("/events/2")
    event_page.book_event(test_data)
    home_page.navigate_to_bookings_from_header()
    bookings_page.wait_for_bookings()
    total_bookings = bookings_page.booking_count()
    print(f"Total bookings before cancellation: {total_bookings}")

    bookings_page.cancel_last_booking()
    bookings_page.booking_count_validation(total_bookings - 1)
    current_bookings = bookings_page.booking_count()
    print(f"Total bookings after cancellation: {current_bookings}")
    if current_bookings != total_bookings - 1:
        print("Booking cancellation failed. The booking card count did not decrease as expected.")
      
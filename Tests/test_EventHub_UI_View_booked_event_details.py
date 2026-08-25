import pytest
from playwright.sync_api import Page
from Pages.bookingsPage import BookingsPage
from Pages.homePage import HomePage
from Pages.loginPage import LoginPage

def test_E2E_view_booked_event_details(page: Page, load_test_data):
    test_data = load_test_data
    login_page = LoginPage(page)
    home_page = HomePage(page)
    bookings_page = BookingsPage(page)

    login_page.login(test_data)
    home_page.navigate_to_bookings_from_header()
    bookings_page.wait_for_bookings()
    bookings_page.view_first_booking_details()
    bookings_page.event_name_validation(test_data)
    bookings_page.check_refund_status(test_data)



    
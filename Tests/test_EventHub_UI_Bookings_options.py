import pytest
from playwright.sync_api import Page
from Pages.bookingsPage import BookingsPage
from Pages.loginPage import LoginPage
from Pages.homePage import HomePage

def test_eventhub_bookings_option1(page: Page, load_test_data):
    test_data = load_test_data
    login_page = LoginPage(page)
    home_page = HomePage(page)
    bookings_page = BookingsPage(page)

    login_page.login(test_data)
    home_page.navigate_to_bookings_from_header()
    bookings_page.bookings_url_validation(test_data)

def test_eventhub_bookings_option2(page: Page, load_test_data):
    test_data = load_test_data
    login_page = LoginPage(page)
    home_page = HomePage(page)
    bookings_page = BookingsPage(page)

    login_page.login(test_data)
    home_page.navigate_to_bookings_from_button()
    bookings_page.bookings_url_validation(test_data)
    
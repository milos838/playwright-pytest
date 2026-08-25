import pytest
from playwright.sync_api import Page
from Pages.eventPage import EventPage
from Pages.loginPage import LoginPage

@pytest.mark.smoke
def test_E2E_book_an_event(page: Page, load_test_data):
    test_data = load_test_data
    login_page = LoginPage(page)
    event_page = EventPage(page)

    login_page.login(test_data)
    event_page.open_event("/events/2")
    event_page.book_event(test_data)
    event_page.booking_confirmation_validation()
   
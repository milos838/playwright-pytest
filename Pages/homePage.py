import pytest
from playwright.sync_api import Page, expect
from Pages.loginPage import LoginPage

class HomePage():

    # Constructor to initialize the page and locators

    def __init__(self, page: Page):
        self.page = page
        self.locator_events_header_link = page.locator("#nav-events")
        self.locator_browse_events = page.get_by_text("Browse Events →")
        self.locator_view_all_events = page.get_by_text("View all →")


    # Functions

    def navigate_to_events_from_header_link(self, load_test_data, login_page: LoginPage):
        login_page = LoginPage(self.page)
        login_page.login(load_test_data)
        self.locator_events_header_link.click()

    def navigate_to_events_from_browseEvents(self, load_test_data, login_page: LoginPage):
        login_page = LoginPage(self.page)
        login_page.login(load_test_data)
        self.locator_browse_events.click()

    def navigate_to_events_from_viewAll(self, load_test_data, login_page: LoginPage):
        login_page = LoginPage(self.page)
        login_page.login(load_test_data)
        self.locator_view_all_events.click()



    # Assertions for home page

    def events_url_validation(self, load_test_data):
        test_data = load_test_data
        expect(self.page).to_have_url(f"{test_data['events_url']}")


import pytest
from playwright.sync_api import Page, expect

class HomePage():

    # Constructor to initialize the page and locators

    def __init__(self, page: Page):
        self.page = page
        self.locator_events_header_link = page.locator("#nav-events")
        self.locator_bookings_header_link = page.locator("#nav-bookings")
        self.locator_browse_events = page.get_by_text("Browse Events →")
        self.locator_view_all_events = page.get_by_text("View all →")
        self.locator_my_bookings_button = page.get_by_role("button", name="My Bookings")


    # Methods

    def navigate_to_events_from_header_link(self):
        self.locator_events_header_link.click()

    def navigate_to_events_from_browseEvents(self):
        self.locator_browse_events.click()

    def navigate_to_events_from_viewAll(self):
        self.locator_view_all_events.click()

    def navigate_to_bookings_from_header(self):
        self.locator_bookings_header_link.click()

    def navigate_to_bookings_from_button(self):
        self.locator_my_bookings_button.click()



    # Assertions for home page

    def events_url_validation(self, load_test_data):
        test_data = load_test_data
        expect(self.page).to_have_url(f"{test_data['events_url']}")


import pytest
from playwright.sync_api import Page, expect

class LoginPage:

    # Constructor to initialize the page and locators

    def __init__(self, page: Page):
        self.page = page
        self.email = self.page.locator("#email")
        self.password = self.page.locator("#password")
        self.login_button = self.page.locator("#login-btn")


    # Functions

    def login(self, load_test_data):
        test_data = load_test_data
        self.page.goto(test_data["url"])
        self.email.fill(test_data["username"])
        self.password.fill(test_data["password"])
        self.login_button.click()

    def navigate_to_URL_(self, load_test_data):
        test_data = load_test_data
        self.page.goto(test_data["url"])
        

    # Assertions for login page 

    def login_validation(self, load_test_data):
        test_data = load_test_data
        expect(self.page.locator("#user-email-display")).to_have_text(test_data["username"])

    def url_validation(self, load_test_data):
        test_data = load_test_data
        expect(self.page).to_have_url(test_data["expected_url"])

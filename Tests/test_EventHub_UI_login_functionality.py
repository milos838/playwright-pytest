import pytest
from playwright.sync_api import Page, expect
from Pages.loginPage import LoginPage

@pytest.mark.smoke
def test_eventhub_ui_login_functionality(page: Page, load_test_data):
    login_page = LoginPage(page)
    login_page.login(load_test_data)
    login_page.login_validation(load_test_data)
    
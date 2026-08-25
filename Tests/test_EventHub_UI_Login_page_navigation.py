import pytest
from playwright.sync_api import Page, expect
from Pages.loginPage import LoginPage


@pytest.mark.smoke
def test_eventHub_login_page_navigation(page: Page, load_test_data): 
    login_page = LoginPage(page)
    login_page.navigate_to_URL_(load_test_data)
    login_page.url_validation(load_test_data)

    

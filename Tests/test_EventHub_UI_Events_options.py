import pytest
from playwright.sync_api import Page, expect
from Pages.loginPage import LoginPage
from Pages.homePage import HomePage

def test_eventhub_events_option(page: Page, load_test_data):
    test_data = load_test_data
    login_page = LoginPage(page)
    home_page = HomePage(page)
    
    login_page.login(test_data)
    home_page.navigate_to_events_from_header_link(test_data, login_page)
    home_page.events_url_validation(test_data)

def test_eventhub_events_browseEvents(page: Page, load_test_data):
    test_data = load_test_data
    login_page = LoginPage(page)
    home_page = HomePage(page)
        
    login_page.login(test_data)
    home_page.navigate_to_events_from_browseEvents(test_data, login_page)
    home_page.events_url_validation(test_data)

def test_eventhub_events_viewAll(page: Page, load_test_data):
    test_data = load_test_data
    login_page = LoginPage(page)
    home_page = HomePage(page)

    login_page.login(test_data)
    home_page.navigate_to_events_from_viewAll(test_data, login_page)
    home_page.events_url_validation(test_data)
    






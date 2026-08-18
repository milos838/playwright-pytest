import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_eventHub_login_page_navigation(page: Page, load_test_data): 
    test_data = load_test_data
    page.goto(test_data["url"])
    expect(page).to_have_url(test_data["expected_url"])

    

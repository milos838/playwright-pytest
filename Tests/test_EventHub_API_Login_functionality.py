import pytest
from playwright.sync_api import Playwright, expect, Page
from Utils.apiBase import APIutils

def test_login_functionality_with_inserted_token(playwright: Playwright, browserInstance: Page, load_test_data):
    api_utils = APIutils()
    getToken = api_utils.getToken(playwright, load_test_data)
    browserInstance.add_init_script(
        f"localStorage.setItem('eventhub_token', '{getToken}')"
    )
    browserInstance.goto(load_test_data["url"])
    expect(browserInstance.get_by_text("Ready to experience something new?")).to_be_visible()
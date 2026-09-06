import pytest
from playwright.sync_api import Playwright, expect, Page
from Utils.apiBase import APIutils

@pytest.mark.smoke
def test_login_functionality_with_inserted_token(playwright: Playwright, page: Page, load_test_data):
    api_utils = APIutils()
    token = api_utils.getToken(playwright, load_test_data)
    page.add_init_script(
        f"localStorage.setItem('eventhub_token', '{token}')"
    )
    page.goto(load_test_data["url"])
    expect(page.get_by_text("Ready to experience something new?")).to_be_visible()
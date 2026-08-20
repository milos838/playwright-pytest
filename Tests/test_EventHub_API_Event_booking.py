import pytest
from playwright.sync_api import Page, expect
from Utils.apiBase import APIutils


@pytest.mark.smoke
def test_book_event_through_api(playwright, page: Page, load_test_data,):

    api_utils = APIutils()
    token = api_utils.getToken(playwright, load_test_data)
    api_utils.bookEvent(playwright, load_test_data)

    page.add_init_script(
        f"window.localStorage.setItem('eventhub_token', '{token}')"
    )

    page.goto(load_test_data["url"])
    page.locator("#nav-bookings").click()
    expect(page.get_by_text("World Tech Summit")).to_be_visible()
    
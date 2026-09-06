from playwright.sync_api import Page, expect


class EventPage:

    def __init__(self, page: Page):
        self.page = page
        self.customer_name = page.locator("#customerName")
        self.customer_email = page.locator("#customer-email")
        self.customer_phone = page.locator("#phone")
        self.confirm_booking_button = page.locator("#confirm-booking")
        self.booking_confirmation = page.locator(".text-xl")

    def open_event(self, event_href: str):
        self.page.locator(f"#book-now-btn[href='{event_href}']").click()

    def book_event(self, test_data: dict):
        self.customer_name.fill(test_data["customer_name"])
        self.customer_email.fill(test_data["customer_email"])
        self.customer_phone.fill(test_data["customer_phone"])
        with self.page.expect_response(
            lambda response: response.request.method == "POST"
            and "/bookings" in response.url
        ) as response_info:
            self.confirm_booking_button.click()
        return response_info.value.json()["data"]["id"]

    def booking_confirmation_validation(self):
        expect(self.booking_confirmation).to_contain_text("Booking Confirmed!")
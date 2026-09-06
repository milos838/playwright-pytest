from playwright.sync_api import Page, expect


class BookingsPage:

    def __init__(self, page: Page):
        self.page = page
        self.booking_cards = page.locator("#booking-card")
        self.refund_button = page.locator("#check-refund-btn")
        self.refund_result = page.locator("#refund-result")
        self.event_name = page.locator(".text-2xl")

    def bookings_url_validation(self, test_data: dict):
        expect(self.page).to_have_url(test_data["bookings_url"])

    def wait_for_bookings(self):
        expect(self.booking_cards.first).to_be_visible(timeout=15000)

    def booking_count(self) -> int:
        return self.booking_cards.count()

    def cancel_last_booking(self):
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.booking_cards.last.locator("#cancel-booking-btn").click()
        self.page.get_by_role("button", name="Yes, cancel it").click()

    def booking_card_for(self, customer_email: str):
        return self.booking_cards.filter(has_text=customer_email)

    def cancel_booking(self, customer_email: str):
        booking_card = self.booking_card_for(customer_email)
        if booking_card.count() == 0:
            return
        self.page.once("dialog", lambda dialog: dialog.accept())
        booking_card.locator("#cancel-booking-btn").click()
        self.page.get_by_role("button", name="Yes, cancel it").click()
        expect(booking_card).to_have_count(0, timeout=15000)

    def view_booking_details(self, customer_email: str):
        self.booking_card_for(customer_email).get_by_role(
            "button", name="View Details"
        ).click()

    def booking_count_validation(self, expected_count: int):
        expect(self.booking_cards).to_have_count(expected_count, timeout=15000)

    def view_first_booking_details(self):
        self.booking_cards.first.get_by_role("button", name="View Details").click()

    def event_name_validation(self, test_data: dict):
        expect(self.event_name).to_contain_text(test_data["event_name"])

    def check_refund_status(self, test_data: dict):
        self.refund_button.click()
        expect(self.refund_result).to_contain_text(test_data["refund_status"])
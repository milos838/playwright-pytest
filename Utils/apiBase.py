from playwright.sync_api import Playwright

eventPayLoad = {"eventId": 1, "quantity": 1}


class APIutils:
    def getToken(self, playwright: Playwright, load_test_data):
        api_request_context = playwright.request.new_context(
            base_url=load_test_data["api_url"]
        )
        try:
            response = api_request_context.post(
                "auth/login",
                data={
                    "email": load_test_data["username"],
                    "password": load_test_data["password"],
                },
            )
            assert response.ok, f"Login request failed status code = {response.status}"
            return response.json()["token"]
        finally:
            api_request_context.dispose()

    def book_event(self, playwright: Playwright, load_test_data):

        token = self.getToken(playwright, load_test_data)

        api_request_context = playwright.request.new_context(
            base_url=load_test_data["api_url"])
        try:
            response = api_request_context.post(
                "bookings",
                data={
                    **eventPayLoad,
                    "customerName": load_test_data["customer_name"],
                    "customerEmail": load_test_data["customer_email"],
                    "customerPhone": load_test_data["customer_phone"],
                },
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                })

            assert response.ok, (
                f"Booking request failed: {response.status} {response.text()}"
            )
            response_body = response.json()
            return response_body["data"]["id"]
        finally:
            api_request_context.dispose()

    bookEvent = book_event


        

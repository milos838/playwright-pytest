from playwright.sync_api import Playwright

eventPayLoad = {
    "eventId": 1,
    "customerName": "John Doe",
    "customerEmail": "test@test.com",
    "customerPhone": "+1234567890",
    "quantity": 1,
}


class APIutils:
    def getToken(self, playwright: Playwright, load_test_data):
        api_request_context = playwright.request.new_context(
            base_url=load_test_data["api_url"]
        )
        response = api_request_context.post(
            "auth/login",
            data={
                "email": load_test_data["username"],
                "password": load_test_data["password"],
            },
        )
        assert response.ok, f"Login request failed status code = {response.status}"
        return response.json()["token"]

    def bookEvent(self, playwright: Playwright, load_test_data):

        token = self.getToken(playwright, load_test_data)

        api_request_context = playwright.request.new_context(
            base_url=load_test_data["api_url"])
        
        response = api_request_context.post(
            "bookings",
            data = eventPayLoad,
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            })
        
        assert response.ok, (
            f"Booking request failed: {response.status} {response.text()}"
        )
        response_body = response.json()
        return response_body["data"]["id"]


        

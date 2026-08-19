from playwright.sync_api import Playwright


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


import pytest
import json
from pathlib import Path


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Default browser context settings for all tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "locale": "en-US",
    }

@pytest.fixture(scope="session")
def load_test_data(data_file: str = "Data/data_setup.json") -> dict:
    """Load test data from a JSON file."""
    data_path = Path(__file__).parent / data_file
    with open(data_path) as f:
        return json.load(f)

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

@pytest.fixture
def browserInstance(playwright, request):
    # Fixture to create new browser instance for each test
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=False)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()

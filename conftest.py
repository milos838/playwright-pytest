import pytest
import json
import os
import re
from uuid import uuid4
from pathlib import Path

from dotenv import load_dotenv
from Pages.bookingsPage import BookingsPage
from Pages.eventPage import EventPage
from Pages.homePage import HomePage
from Pages.loginPage import LoginPage
from Utils.apiBase import APIutils


load_dotenv(Path(__file__).parent / ".env")


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
    with open(data_path, encoding="utf-8") as f:
        test_data = json.load(f)

    test_data["url"] = os.getenv("EVENTHUB_URL", test_data["url"])
    test_data["api_url"] = os.getenv("EVENTHUB_API_URL", test_data["api_url"])
    test_data["username"] = os.getenv("EVENTHUB_USERNAME")
    test_data["password"] = os.getenv("EVENTHUB_PASSWORD")
    if not test_data["username"] or not test_data["password"]:
        raise pytest.UsageError(
            "Set EVENTHUB_USERNAME and EVENTHUB_PASSWORD before running tests."
        )
    return test_data


@pytest.fixture
def booking_data(load_test_data):
    """Return unique booking details so workers never submit identical data."""
    worker_id = os.getenv("PYTEST_XDIST_WORKER", "master")
    unique_id = f"{worker_id}-{uuid4().hex[:8]}"
    return {
        **load_test_data,
        "customer_name": f"{load_test_data['customer_name']} {unique_id}",
        "customer_email": f"{unique_id}@example.test",
        "customer_phone": f"+1555{uuid4().int % 10_000_000:07d}",
    }


def pytest_addoption(parser):
    parser.addoption(
        "--allow-destructive-cleanup",
        action="store_true",
        help="Allow the test that clears every booking for the account to run.",
    )


@pytest.fixture
def isolated_ui_booking(page, booking_data):
    """Create one booking for a test and remove only that booking afterward."""
    LoginPage(page).login(booking_data)
    EventPage(page).open_event("/events/2")
    EventPage(page).book_event(booking_data)
    EventPage(page).booking_confirmation_validation()

    yield booking_data

    page.goto(booking_data["url"])
    LoginPage(page).login(booking_data)
    HomePage(page).navigate_to_bookings_from_header()
    BookingsPage(page).cancel_booking(booking_data["customer_email"])


@pytest.fixture
def isolated_api_booking(playwright, page, booking_data):
    """Create an API booking and remove only that booking through the UI."""
    api_utils = APIutils()
    token = api_utils.getToken(playwright, booking_data)
    api_utils.book_event(playwright, booking_data)
    yield token, booking_data

    page.add_init_script(
        f"window.localStorage.setItem('eventhub_token', '{token}')"
    )
    page.goto(booking_data["url"])
    page.locator("#nav-bookings").click()
    BookingsPage(page).cancel_booking(booking_data["customer_email"])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def trace_failed_test(context, request):
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )

    yield

    test_failed = any(
        getattr(request.node, report_name, None) is not None
        and getattr(request.node, report_name).failed
        for report_name in ("rep_setup", "rep_call")
    )

    if test_failed:
        trace_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.node.nodeid)
        trace_path = Path("test-results") / "traces" / f"{trace_name}.zip"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        context.tracing.stop(path=str(trace_path))
    else:
        context.tracing.stop()

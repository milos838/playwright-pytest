import pytest
import json
import re
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
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)


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

# EventHub Playwright End-to-End Testing Suite

## Project Overview

This project is an end-to-end (E2E) test automation framework for the **EventHub application**, a web-based event booking platform. The test suite is built using **Playwright** and **pytest**, providing comprehensive automated testing coverage for user workflows including login, event browsing, event booking, and booking management.

**Application Under Test:** [EventHub - Rahul Shetty Academy](https://eventhub.rahulshettyacademy.com/)

---

## Project Purpose

The automation test suite validates critical user workflows in the EventHub application:
- User authentication and login functionality
- Event browsing and discovery
- Event booking process
- Booking management (viewing and canceling bookings)
- Page navigation
- UI element visibility and correctness

---

## Technology Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | ≥3.10 | Test programming language |
| **Playwright** | ≥1.49.0 | Browser automation framework |
| **pytest** | ≥8.0.0 | Test framework and runner |
| **pytest-playwright** | ≥0.6.0 | pytest plugin for Playwright integration |

---

## Failed Test Traces

Playwright tracing starts automatically for every test. Traces are saved only for failed setup or test phases in `test-results/traces/`.

Open a trace with:

```bash
playwright show-trace test-results/traces/<trace-file>.zip
```

Successful tests stop tracing without creating an artifact.

---

## Project Structure

```
playwright-pytest/
├── conftest.py                                 # pytest configuration and fixtures
├── pyproject.toml                              # Project metadata and dependencies
├── Data/
│   └── data_setup.json                         # Test data and configuration
├── Pages/                                      # Page Object Models
│   ├── loginPage.py                            # Login and authentication
│   ├── homePage.py                             # Home-page navigation
│   ├── eventPage.py                            # Event booking workflow
│   └── bookingsPage.py                         # Booking management workflows
├── Utils/                                      # Shared utilities
│   └── apiBase.py                              # API helpers
├── Tests/                                      # Test cases
│   ├── test_EventHub_UI_Login_page_navigation.py # Login page navigation tests
│   ├── test_EventHub_UI_login_functionality.py # Login functionality tests
│   ├── test_EventHub_UI_Events_options.py      # Event browsing tests
│   ├── test_EventHub_UI_Bookings_options.py    # Booking management tests
│   ├── test_EventHub_UI_Event_booking.py       # Event booking tests
│   ├── test_EventHub_UI_Cancel_booked_event.py # Cancel booking tests
│   ├── test_EventHub_UI_View_booked_event_details.py # View booking details tests
│   ├── test_EventHub_API_Login_functionality.py # API login tests
│   ├── test_EventHub_API_Event_booking.py      # API booking tests
│   └── test_EventHub_Clearing_test_data.py     # Test-data cleanup
└── playwright_pytest.egg-info/                 # Package metadata
```

---

## Prerequisites

- **Python 3.10+** installed on your system
- **pip** package manager
- **Virtual environment** (recommended: venv or poetry)
- A supported browser (Chromium is configured by default)

---

## Installation and Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd playwright-pytest
```

### 2. Create a Virtual Environment
```bash
# Using venv
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -e .
```

This installs:
- `playwright>=1.49.0` - Browser automation
- `pytest>=8.0.0` - Test framework
- `pytest-playwright>=0.6.0` - pytest integration

### 4. Install Playwright Browsers
```bash
playwright install chromium
# Or install all supported browsers:
playwright install
```

---

## Configuration

### pytest Configuration (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]               # Directory containing tests
addopts = ["--strict-markers", "--strict-config", "-ra"]
markers = [
    "smoke: quick sanity checks",   # Mark for smoke tests
    "slow: tests that take longer to run"  # Mark for slow tests
]

[tool.pytest-playwright]
browser = "chromium"                # Browser to use
headed = false                      # Run in headless mode
slow_mo = 0                         # No delay between actions
```

### Browser Context Settings (`conftest.py`)

Each test runs with:
- **Viewport:** 1280×720 pixels
- **Locale:** en-US

---

## Test Data

Test data is stored in `Data/data_setup.json`:

```json
{
    "url": "https://eventhub.rahulshettyacademy.com/",
    "expected_url": "https://eventhub.rahulshettyacademy.com/login",
    "events_url": "https://eventhub.rahulshettyacademy.com/events",
    "bookings_url": "https://eventhub.rahulshettyacademy.com/bookings",
    "event_name": "Hollywood Monsoon Night — Los Angeles",
    "customer_name": "John Doe",
    "customer_email": "test@test.com",
    "customer_phone": "+1234567890",
    "refund_status": "Eligible for refund."
}
```

Set the account credentials outside the repository before running tests:

```bash
# macOS/Linux
export EVENTHUB_USERNAME="your-test-account@example.com"
export EVENTHUB_PASSWORD="your-test-password"

# Windows PowerShell
$env:EVENTHUB_USERNAME = "your-test-account@example.com"
$env:EVENTHUB_PASSWORD = "your-test-password"
```

Booking tests generate unique customer details per test and clean up only the
booking they created, which allows parallel execution with `pytest-xdist`.

Run against a specific browser with the standard Playwright options:

```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
pytest -n auto --browser chromium
```

**Important:** This file contains test credentials. Do not commit real credentials to version control. Use environment variables or secrets management in production environments.

---

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest Tests/test_EventHub_UI_login_functionality.py
```

### Run Specific Test
```bash
pytest Tests/test_EventHub_UI_login_functionality.py::test_eventhub_ui_login_functionality
```

### Run Tests with Specific Marker
```bash
# Run only smoke tests
pytest -m smoke

# Run only slow tests
pytest -m slow
```

### Run Tests in Headed Mode (see browser)
```bash
pytest --headed
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Detailed Output and Print Statements
```bash
pytest -vv -s
```

### Generate HTML Report
```bash
pytest --html=report.html --self-contained-html
```

---

## Test Cases Overview

### 1. Login Page Navigation
**File:** `test_EventHub_Login_page_navigation.py`

**Purpose:** Verify that navigating to EventHub redirects to the login page.

**Test:** `test_eventHub_login_page_navigation`
- Navigate to EventHub home page
- Assert that the current URL is the login page

---

### 2. Login Functionality
**File:** `test_EventHub_UI_login_functionality.py`

**Purpose:** Validate user login with correct credentials.

**Test:** `test_eventhub_ui_login_functionality`
- Navigate to EventHub home page
- Enter valid email address
- Enter valid password
- Click login button
- Assert that user email is displayed on the page

---

### 3. Event Booking
**File:** `test_EventHub_UI_Event_booking.py`

**Purpose:** Complete end-to-end event booking workflow.

**Test:** `test_E2E_book_an_event`
- Login with valid credentials
- Click "Book Now" button for an event (Event ID: 2)
- Fill in customer details (name, email, phone)
- Confirm booking
- Assert "Booking Confirmed!" message is displayed

**Workflow Steps:**
1. Authentication
2. Event selection
3. Customer information entry
4. Booking confirmation
5. Success verification

---

### 4. Event Browsing
**File:** `test_EventHub_Events_options.py`

**Purpose:** Test event browsing and listing functionality.

---

### 5. Booking Management
**File:** `test_EventHub_Bookings_options.py`

**Purpose:** Test booking management features.

---

### 6. View Booking Details
**File:** `test_EventHub_UI_View_booked_event_details.py`

**Purpose:** Verify viewing detailed information about booked events.

---

### 7. Cancel Booking
**File:** `test_EventHub_UI_Cancel_booked_event.py`

**Purpose:** Test canceling previously booked events.

---

## Test Fixtures

### `browser_context_args`
**Scope:** Session

Configures the browser context for all tests with:
- Standard viewport size (1280×720)
- US English locale
- Other default browser settings

**Usage:** Automatically applied to all tests via pytest-playwright plugin

### `load_test_data`
**Scope:** Session

Loads test configuration and data from `Data/data_setup.json`.

**Usage:**
```python
def test_example(page: Page, load_test_data):
    test_data = load_test_data
    # Access data: test_data["username"], test_data["password"], etc.
```

---

## Page Object Model (POM) Pattern

UI tests use page objects to keep locators, browser actions, and page-level assertions out of the test files.

### Example Structure
```
Pages/
├── loginPage.py       # Login and authentication
├── homePage.py        # Home-page navigation
├── eventPage.py       # Event booking workflow
└── bookingsPage.py    # Bookings, cancellation, details, and refunds
```

Each test creates the page objects with the shared Playwright `page` fixture. Authentication is performed once through `LoginPage`; navigation and workflow actions are then delegated to the relevant page object.

### Example Page Object Usage
```python
login_page = LoginPage(page)
home_page = HomePage(page)

login_page.login(test_data)
home_page.navigate_to_events_from_header_link()
```

---

## Utility Functions

The `Utils/` directory is currently empty. Consider adding utilities for:
- **Common actions:** Click, fill, wait, scroll
- **Assertions:** Custom verification methods
- **Data generation:** Test data creation and validation
- **Logging:** Test execution logging
- **Screenshot capture:** For failed tests

---

## Best Practices

### 1. **Locator Strategy**
- Use unique, stable selectors (IDs preferred over CSS classes)
- Avoid hardcoded waits; use Playwright's auto-waiting
- Prefer semantic selectors when possible

### 2. **Test Independence**
- Each test should be independent and not rely on test execution order
- Use fixtures to set up required state
- Clean up resources after tests

### 3. **Test Data Management**
- Keep test data externalized (JSON, CSV, environment variables)
- Never hardcode sensitive credentials in test files
- Use environment-specific configuration files

### 4. **Assertions**
- Use Playwright's `expect()` API with timeout-aware assertions
- Provide meaningful error messages
- Avoid generic assertions

### 5. **Error Handling**
- Capture screenshots on test failure (configure in pytest plugin)
- Log relevant information for debugging
- Use descriptive test names

### 6. **Performance**
- Run tests in parallel when possible: `pytest -n auto`
- Use appropriate timeouts
- Avoid unnecessary waits or sleeps

### 7. **Maintenance**
- Keep tests DRY (Don't Repeat Yourself)
- Implement Page Object Model for complex applications
- Update tests when UI changes
- Regular test review and refactoring

---

## Troubleshooting

### Issue: Playwright Browsers Not Found
```bash
# Solution: Install browsers
playwright install
# Or install specific browser
playwright install chromium
```

### Issue: Tests Fail Due to Timeout
```bash
# Increase timeout in conftest.py or use in test:
page.set_default_timeout(10000)  # 10 seconds
```

### Issue: Login Fails
- Verify credentials in `data_setup.json` are correct
- Check if the application URL is accessible
- Verify network connectivity
- Check if the login page elements have changed

### Issue: Element Not Found
```python
# Wait for element to be visible
page.locator("#element-id").wait_for(state="visible", timeout=5000)
```

### Issue: Port Already in Use
- Close any existing Playwright browser instances
- Clear port by running: `lsof -i :PORT` (macOS/Linux)

### Enable Debug Mode
```bash
# Run with debug logging
PWDEBUG=1 pytest

# Or use Playwright Inspector
playwright codegen https://eventhub.rahulshettyacademy.com/
```

---

## Continuous Integration

### GitHub Actions Example
```yaml
name: Playwright Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -e .
      - run: playwright install chromium
      - run: pytest -m smoke
```

---

## Future Enhancements

1. **Add Visual Testing** - Screenshot comparison with baseline images
2. **Parallel Execution** - Configure pytest-xdist for parallel test runs
3. **Test Reporting** - Add Allure or HTML reporting
4. **CI/CD Integration** - Set up GitHub Actions or similar
5. **Performance Testing** - Add performance metrics and benchmarks
6. **API Testing** - Combine with API testing for full coverage
7. **Data-Driven Tests** - Parameterize tests with multiple data sets
8. **Cross-Browser Testing** - Test on Firefox, Safari, Edge
9. **Mobile Testing** - Add mobile device emulation tests

---

## Contributing

When adding new tests:
1. Follow existing naming conventions
2. Use appropriate pytest markers (@pytest.mark.smoke, etc.)
3. Include docstrings explaining test purpose
4. Use the `load_test_data` fixture for test data
5. Implement Page Object Model if creating new pages
6. Update this documentation with new test cases

---

## Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-playwright Plugin](https://playwright.dev/python/docs/pytest)
- [EventHub Application](https://eventhub.rahulshettyacademy.com/)
- [Best Practices for Test Automation](https://playwright.dev/python/docs/intro)

---

## License

This project is part of the test automation learning series from Rahul Shetty Academy.

---

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review Playwright documentation
3. Enable debug mode to gather detailed logs
4. Check application status and accessibility

---

**Last Updated:** August 18, 2026  
**Project Version:** 0.1.0  
**Python Version:** ≥3.10

# Test Writing and Execution Guide

## Table of Contents
1. [Test Structure](#test-structure)
2. [Writing New Tests](#writing-new-tests)
3. [Running Tests](#running-tests)
4. [Test Organization](#test-organization)
5. [Common Patterns](#common-patterns)
6. [Debugging Tests](#debugging-tests)
7. [Test Best Practices](#test-best-practices)

---

## Test Structure

### Basic Test Anatomy

Every test file follows this structure:

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke  # Optional: test marker
def test_descriptive_test_name(page: Page, load_test_data):
    """
    Docstring explaining what this test does.
    This is important for documentation.
    """
    test_data = load_test_data
    
    # Setup: Prepare the test environment
    page.goto(test_data["url"])
    
    # Action: Perform the action being tested
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    page.locator("#login-btn").click()
    
    # Assert: Verify the expected outcome
    expect(page.locator("#user-email-display")).to_have_text(test_data["username"])
```

### Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Import** | Import required modules | `from playwright.sync_api import Page` |
| **Decorator** | Mark test behavior | `@pytest.mark.smoke` |
| **Function Name** | Test identifier | `test_login_with_valid_credentials` |
| **Docstring** | Test documentation | `"""Verify login with correct credentials."""` |
| **Fixture** | Test data/setup | `page: Page, load_test_data` |
| **Setup** | Prepare state | `page.goto(url)` |
| **Action** | Perform operation | `page.locator("#btn").click()` |
| **Assert** | Verify result | `expect(locator).to_have_text("Success")` |

---

## Writing New Tests

### Step 1: Choose Test Location

Tests go in the `Tests/` directory:
```
Tests/
├── test_EventHub_Login_*.py        # Login-related tests
├── test_EventHub_UI_*.py           # UI interaction tests
├── test_EventHub_Bookings_*.py     # Booking-related tests
└── test_EventHub_Events_*.py       # Event-related tests
```

**Naming Convention:** `test_<feature>_<scenario>.py`

Examples:
- `test_EventHub_Login_valid_credentials.py`
- `test_EventHub_UI_Event_booking_confirmation.py`
- `test_EventHub_Bookings_cancel_refund.py`

### Step 2: Create Test File

**File: Tests/test_EventHub_Login_valid_credentials.py**

```python
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_login_with_valid_credentials(page: Page, load_test_data):
    """
    Test: User can log in with valid email and password.
    
    Scenario:
    1. Navigate to EventHub application
    2. Enter valid email address
    3. Enter valid password
    4. Click login button
    5. Verify user is logged in (email displayed)
    
    Expected Result:
    User's email is displayed on the dashboard, confirming successful login.
    """
    test_data = load_test_data
    
    # Navigate to application
    page.goto(test_data["url"])
    
    # Fill login form
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    
    # Submit form
    page.locator("#login-btn").click()
    
    # Verify login success
    expect(page.locator("#user-email-display")).to_have_text(test_data["username"])
```

### Step 3: Use Fixtures

Fixtures provide test data and setup. Available fixtures:

#### `page: Page`
The Playwright page object for browser interaction.
```python
def test_example(page: Page):
    page.goto("https://example.com")
    page.locator("button").click()
```

#### `load_test_data`
Loads test data from `Data/data_setup.json`.
```python
def test_example(page: Page, load_test_data):
    test_data = load_test_data
    username = test_data["username"]
    password = test_data["password"]
```

#### `browser_context_args`
Session-scoped fixture providing browser context settings.
```python
# Automatically applied, no need to explicitly use
# Default viewport: 1280×720, Locale: en-US
```

### Step 4: Add Test Logic

#### Navigation
```python
# Go to URL
page.goto(test_data["url"])

# Go back
page.go_back()

# Go forward
page.go_forward()

# Reload
page.reload()
```

#### Element Interaction

**Locate Elements:**
```python
# By ID
page.locator("#element-id")

# By CSS class
page.locator(".class-name")

# By attribute
page.locator('[data-test="value"]')

# By text
page.locator("text=Click me")

# By XPath (last resort)
page.locator("xpath=//div[@class='item']")
```

**Fill Input:**
```python
page.locator("#email").fill("test@example.com")
page.locator("#password").type("password", delay=100)  # Type with delay
```

**Click Elements:**
```python
page.locator("#button").click()
page.locator("#button").double_click()
page.locator("#button").click(modifiers=["Control"])  # With modifier
```

**Select Dropdown:**
```python
page.locator("select").select_option("value")
page.locator("select").select_option(label="Option Text")
```

**Check/Uncheck Checkbox:**
```python
page.locator("#checkbox").check()
page.locator("#checkbox").uncheck()
page.locator("#checkbox").set_checked(True)
```

**Select Radio Button:**
```python
page.locator('input[name="option"][value="choice1"]').check()
```

#### Wait for Elements

**Wait for element visibility:**
```python
page.locator("#element").wait_for(state="visible", timeout=5000)
```

**Wait for element to be hidden:**
```python
page.locator("#loader").wait_for(state="hidden", timeout=5000)
```

**Wait for navigation:**
```python
with page.expect_navigation():
    page.locator("#link").click()
```

**Wait for specific URL:**
```python
page.wait_for_url(test_data["bookings_url"])
```

#### Assertions

**Text Assertions:**
```python
expect(page.locator("#message")).to_have_text("Success!")
expect(page.locator("#message")).to_contain_text("Success")
```

**Visibility Assertions:**
```python
expect(page.locator("#element")).to_be_visible()
expect(page.locator("#element")).to_be_hidden()
```

**Enabled/Disabled Assertions:**
```python
expect(page.locator("#button")).to_be_enabled()
expect(page.locator("#button")).to_be_disabled()
```

**Checked Assertions:**
```python
expect(page.locator("#checkbox")).to_be_checked()
expect(page.locator("#checkbox")).not_to_be_checked()
```

**URL Assertions:**
```python
expect(page).to_have_url(test_data["bookings_url"])
```

**Count Assertions:**
```python
expect(page.locator(".item")).to_have_count(5)
```

**Attribute Assertions:**
```python
expect(page.locator("#input")).to_have_attribute("placeholder", "Enter text")
```

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

### Run Specific Test Function
```bash
pytest Tests/test_EventHub_UI_login_functionality.py::test_eventhub_ui_login_functionality
```

### Run Multiple Files
```bash
pytest Tests/test_EventHub_UI_*.py
```

### Run with Markers
```bash
# Run only smoke tests
pytest -m smoke

# Run everything except slow tests
pytest -m "not slow"

# Run smoke AND another marker
pytest -m "smoke and login"
```

### Run with Different Browsers
```bash
# Default is chromium (set in pyproject.toml)
pytest

# Override with command line
pytest --browser firefox
pytest --browser webkit
```

### Run in Headed Mode (see browser)
```bash
pytest --headed

# Run specific test in headed mode
pytest Tests/test_EventHub_UI_login_functionality.py --headed
```

### Run with Verbose Output
```bash
# Normal verbose
pytest -v

# Extra verbose (shows all assertions)
pytest -vv

# Show print statements and logs
pytest -s

# Combination
pytest -vvs
```

### Run with Timing Information
```bash
# Show slowest tests
pytest --durations=10

# Show all tests with execution time
pytest -v --durations=0
```

### Run with Retries
```bash
# Install pytest-rerunfailures
pip install pytest-rerunfailures

# Rerun failed tests up to 3 times
pytest --reruns 3
```

### Generate Reports

**HTML Report:**
```bash
# Install pytest-html
pip install pytest-html

# Generate report
pytest --html=report.html --self-contained-html

# Open report
# Windows
start report.html
# macOS
open report.html
# Linux
xdg-open report.html
```

**JUnit XML Report:**
```bash
pytest --junit-xml=results.xml
```

**Coverage Report:**
```bash
# Install pytest-cov
pip install pytest-cov

# Generate coverage
pytest --cov=Tests --cov-report=html

# Open coverage report
# Windows
start htmlcov/index.html
```

---

## Test Organization

### By Feature
Organize tests by application feature:
```
Tests/
├── test_EventHub_Login_*.py
├── test_EventHub_Events_*.py
├── test_EventHub_Bookings_*.py
└── test_EventHub_UI_*.py
```

### By Test Type
```
Tests/
├── functional/     # Feature tests
│   ├── test_login.py
│   └── test_booking.py
├── ui/            # UI interaction tests
│   ├── test_navigation.py
│   └── test_forms.py
└── negative/      # Error handling tests
    ├── test_invalid_login.py
    └── test_form_validation.py
```

### Using Pytest Classes
Group related tests:
```python
class TestLoginFunctionality:
    """Tests for EventHub login feature."""
    
    def test_login_with_valid_credentials(self, page, load_test_data):
        """Test successful login."""
        pass
    
    def test_login_with_invalid_email(self, page):
        """Test login with invalid email format."""
        pass
    
    def test_login_with_empty_password(self, page):
        """Test login with empty password."""
        pass


class TestEventBooking:
    """Tests for event booking workflow."""
    
    def test_book_event_complete_workflow(self, page, load_test_data):
        """Test complete event booking."""
        pass
```

---

## Common Patterns

### Pattern: Login Before Test

**Fixture for authenticated page:**
```python
# In conftest.py
@pytest.fixture
def authenticated_page(page, load_test_data):
    """Provide a page already logged in."""
    test_data = load_test_data
    page.goto(test_data["url"])
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    page.locator("#login-btn").click()
    page.wait_for_url(test_data["bookings_url"])
    return page

# In test file
def test_view_booked_event(authenticated_page):
    """Test that user can view booked event."""
    authenticated_page.locator(".booked-event").click()
    expect(authenticated_page.locator("#event-details")).to_be_visible()
```

### Pattern: Data-Driven Tests

**Using pytest.mark.parametrize:**
```python
@pytest.mark.parametrize("email,password", [
    ("valid@example.com", "Password123"),
    ("another@example.com", "SecurePass456"),
])
def test_login_multiple_users(page, email, password):
    """Test login with different credentials."""
    page.goto("https://eventhub.rahulshettyacademy.com/")
    page.locator("#email").fill(email)
    page.locator("#password").fill(password)
    page.locator("#login-btn").click()
    expect(page.locator("#user-email-display")).to_have_text(email)
```

### Pattern: Capturing Screenshots

**On test failure:**
```bash
# Automatic in pytest-playwright
pytest --screenshot=only-on-failure
```

**Manual screenshots:**
```python
def test_with_screenshot(page):
    page.goto("https://eventhub.rahulshettyacademy.com/")
    page.screenshot(path="screenshot.png")
    page.locator("#button").click()
    page.screenshot(path="after-click.png")
```

### Pattern: Handling Multiple Elements

```python
def test_all_events_displayed(page):
    """Test that all events are displayed."""
    events = page.locator(".event-card")
    
    # Count elements
    count = events.count()
    assert count > 0
    
    # Iterate over elements
    for i in range(count):
        event = events.nth(i)
        expect(event).to_be_visible()
        
        # Get text
        event_title = event.locator(".event-title").text_content()
        assert event_title
```

### Pattern: Modal/Dialog Handling

```python
def test_confirm_booking_modal(page, load_test_data):
    """Test confirming booking in modal."""
    # Trigger modal
    page.locator("#book-btn").click()
    
    # Wait for modal
    modal = page.locator(".modal")
    expect(modal).to_be_visible()
    
    # Fill form in modal
    page.locator(".modal #customer-name").fill(load_test_data["customer_name"])
    page.locator(".modal #confirm-btn").click()
    
    # Verify modal closed
    expect(modal).to_be_hidden()
```

### Pattern: Error Handling

```python
def test_handles_network_error(page):
    """Test graceful handling of network error."""
    # Simulate network error
    page.context.add_route("**/*", lambda route: route.abort())
    
    page.goto("https://eventhub.rahulshettyacademy.com/")
    
    # Verify error message displayed
    expect(page.locator(".error-message")).to_be_visible()
    
    # Clean up route
    page.context.remove_route("**/*")
```

---

## Debugging Tests

### Enable Debug Mode

```bash
# Windows PowerShell
$env:PWDEBUG = 1
pytest Tests/test_file.py

# Windows Command Prompt
set PWDEBUG=1
pytest Tests/test_file.py

# macOS/Linux
PWDEBUG=1 pytest Tests/test_file.py
```

This launches Playwright Inspector for step-by-step debugging.

### Add Print Statements

```python
def test_debug_example(page, load_test_data):
    print("Starting test")
    page.goto(load_test_data["url"])
    print(f"Page title: {page.title()}")
    
    page.locator("#email").fill("test@example.com")
    print("Email filled")
    
    page.locator("#login-btn").click()
    print("Login button clicked")
```

Run with `-s` flag to see output:
```bash
pytest -s Tests/test_debug_example.py
```

### Use pdb (Python Debugger)

```python
def test_with_debugger(page):
    page.goto("https://example.com")
    import pdb; pdb.set_trace()  # Execution pauses here
    page.locator("#button").click()
```

Run test and interact with debugger:
```bash
pytest -s Tests/test_with_debugger.py
```

### Take Screenshots and Videos

```python
# In conftest.py - auto-capture on failure
@pytest.fixture
def page(page):
    # Screenshot on failure
    page.on("close", lambda p: p.screenshot(path=f"screenshot-{time.time()}.png"))
    return page

# In test
page.video.path()  # Get video file path
```

### Increase Timeouts

```python
def test_slow_page(page):
    page.set_default_timeout(30000)  # 30 seconds
    page.goto("https://slow-site.example.com")
    page.wait_for_load_state("networkidle")
```

### Use Playwright Codegen

Generate test code by recording interactions:
```bash
playwright codegen https://eventhub.rahulshettyacademy.com/
```

This opens a browser where you interact with the site, and Playwright generates the corresponding test code.

### Check Selector

Verify that your locators are correct:
```python
def test_find_element(page):
    # Method 1: Using Playwright Inspector
    elements = page.locator("#email")
    
    # Method 2: Check count
    count = elements.count()
    print(f"Found {count} elements matching '#email'")
    
    # Method 3: Check visibility
    if elements.is_visible():
        print("Element is visible")
    else:
        print("Element is hidden")
```

---

## Test Best Practices

### ✅ DO

1. **Use descriptive test names**
   ```python
   # Good
   def test_login_with_valid_email_and_password(page, load_test_data):
       pass
   
   # Bad
   def test_1(page, load_test_data):
       pass
   ```

2. **Add docstrings**
   ```python
   def test_book_event(page, load_test_data):
       """
       Test booking an event end-to-end.
       
       Steps:
       1. Login with valid credentials
       2. Navigate to events
       3. Book an event
       4. Verify booking confirmation
       """
   ```

3. **Use Playwright's built-in waits**
   ```python
   # Good - auto-waits
   page.locator("#element").click()
   
   # Avoid - manual wait
   import time
   time.sleep(2)
   ```

4. **Keep tests focused**
   ```python
   # Good - tests one thing
   def test_login_displays_email(page, load_test_data):
       page.goto(load_test_data["url"])
       page.locator("#email").fill(load_test_data["username"])
       page.locator("#password").fill(load_test_data["password"])
       page.locator("#login-btn").click()
       expect(page.locator("#user-email-display")).to_have_text(load_test_data["username"])
   ```

5. **Use fixtures for repeated setup**
   ```python
   # Good - reusable fixture
   @pytest.fixture
   def logged_in_page(page, load_test_data):
       # Setup login...
       return page
   ```

6. **Use appropriate markers**
   ```python
   @pytest.mark.smoke
   def test_critical_feature(page):
       pass
   
   @pytest.mark.slow
   def test_long_running_feature(page):
       pass
   ```

### ❌ DON'T

1. **Don't use hard waits**
   ```python
   # Bad
   import time
   time.sleep(2)
   
   # Good
   page.wait_for_url(expected_url)
   ```

2. **Don't test multiple features in one test**
   ```python
   # Bad - tests login AND booking AND cancellation
   def test_everything(page, load_test_data):
       # login
       # book event
       # cancel booking
   ```

3. **Don't rely on test execution order**
   ```python
   # Bad - test depends on previous test
   def test_1():
       page.goto("url")
   
   def test_2():
       # Assumes test_1 has run
       page.locator("#button").click()
   ```

4. **Don't hardcode values**
   ```python
   # Bad
   page.locator("#email").fill("test@example.com")
   
   # Good
   page.locator("#email").fill(load_test_data["username"])
   ```

5. **Don't ignore failed assertions**
   ```python
   # Bad
   try:
       expect(element).to_be_visible()
   except:
       pass  # Silently ignore failure
   ```

---

## Quick Reference Commands

| Task | Command |
|------|---------|
| Run all tests | `pytest` |
| Run smoke tests | `pytest -m smoke` |
| Run with verbose | `pytest -v` |
| Run in headed mode | `pytest --headed` |
| Run specific test | `pytest Tests/test_file.py::test_name` |
| Run with print output | `pytest -s` |
| Debug test | `PWDEBUG=1 pytest -s Tests/test.py` |
| Generate HTML report | `pytest --html=report.html --self-contained-html` |
| Run with retries | `pytest --reruns 3` |
| Show slowest tests | `pytest --durations=10` |

---

**Last Updated:** August 18, 2026  
**Test Framework:** Playwright + pytest

# Quick Reference Card

## Setup (One-Time)

```bash
# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -e .

# Install browsers
playwright install chromium
```

---

## Running Tests

```bash
# All tests
pytest

# Specific test file
pytest Tests/test_file.py

# Specific test function
pytest Tests/test_file.py::test_function_name

# Smoke tests only
pytest -m smoke

# With verbose output
pytest -v

# Show print statements
pytest -s

# Headed mode (see browser)
pytest --headed

# Debug mode
PWDEBUG=1 pytest -s Tests/test_file.py

# Generate HTML report
pytest --html=report.html --self-contained-html

# Show slowest tests
pytest --durations=10

# Run with timing
pytest -v --durations=0
```

---

## Test File Template

```python
"""Test module description."""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_feature_scenario(page: Page, load_test_data):
    """Test description and expected result."""
    test_data = load_test_data
    
    # SETUP
    page.goto(test_data["url"])
    
    # ACTION
    page.locator("#selector").fill("value")
    page.locator("#button").click()
    
    # ASSERT
    expect(page.locator("#result")).to_have_text("Expected")
```

---

## Common Locator Patterns

```python
# By ID
page.locator("#element-id")

# By class
page.locator(".class-name")

# By attribute
page.locator('[data-test="value"]')

# By text
page.locator("text=Click me")

# By XPath
page.locator("xpath=//div[@class='item']")
```

---

## Common Actions

```python
# Navigation
page.goto(url)
page.go_back()
page.go_forward()
page.reload()

# Input
page.locator("#email").fill("test@example.com")
page.locator("#password").type("password")

# Click
page.locator("#button").click()
page.locator("#button").double_click()

# Select
page.locator("select").select_option("value")

# Checkbox/Radio
page.locator("#checkbox").check()
page.locator("#checkbox").uncheck()
```

---

## Common Assertions

```python
# Text
expect(locator).to_have_text("text")
expect(locator).to_contain_text("text")

# Visibility
expect(locator).to_be_visible()
expect(locator).to_be_hidden()

# Enabled/Disabled
expect(locator).to_be_enabled()
expect(locator).to_be_disabled()

# Checked
expect(locator).to_be_checked()
expect(locator).not_to_be_checked()

# URL
expect(page).to_have_url("https://...")

# Count
expect(locator).to_have_count(5)

# Attribute
expect(locator).to_have_attribute("name", "value")
```

---

## Waiting

```python
# Wait for element visibility
page.locator("#element").wait_for(state="visible", timeout=5000)

# Wait for URL
page.wait_for_url("expected-url")

# Wait for navigation
with page.expect_navigation():
    page.locator("#link").click()

# Wait for load state
page.wait_for_load_state("networkidle")
```

---

## Files and Locations

| What | Where |
|------|-------|
| Tests | `Tests/` |
| Test Data | `Data/data_setup.json` |
| Configuration | `pyproject.toml`, `conftest.py` |
| Documentation | `README.md`, `SETUP.md`, etc. |
| Page Objects | `Pages/` (empty, ready to use) |
| Utilities | `Utils/` (empty, ready to use) |

---

## Configuration

### Run in Headed Mode Temporarily
```bash
pytest --headed
```

### Add Delay Between Actions
```bash
pytest --slowmo=1000  # 1 second
```

### Change Browser
```bash
pytest --browser firefox
pytest --browser webkit
```

### Run Parallel Tests
```bash
pip install pytest-xdist
pytest -n auto  # Use all CPU cores
```

---

## Test Markers

```python
@pytest.mark.smoke    # Quick critical tests
@pytest.mark.slow     # Long-running tests
```

Run by marker:
```bash
pytest -m smoke           # Only smoke tests
pytest -m "not slow"      # Everything except slow
pytest -m "smoke and ui"  # Multiple markers
```

---

## Debugging

### Print Output
```python
print("Debug message")
```

Run with: `pytest -s`

### Step Through Code
```python
import pdb; pdb.set_trace()
```

### Enable Full Debug
```bash
PWDEBUG=1 pytest -s Tests/test_file.py
```

### Record Browser Interaction
```bash
playwright codegen https://eventhub.rahulshettyacademy.com/
```

---

## Project Structure

```
playwright-pytest/
├── conftest.py              # Fixtures and config
├── pyproject.toml           # Dependencies
├── Data/
│   └── data_setup.json      # Test data
├── Tests/
│   └── test_*.py            # Test files
├── Pages/                   # Page Objects (empty)
├── Utils/                   # Utilities (empty)
├── README.md                # Main docs
├── SETUP.md                 # Installation
├── TEST_GUIDE.md            # Test writing
├── ARCHITECTURE.md          # Design
├── CONTRIBUTING.md          # Guidelines
└── INDEX.md                 # Doc index
```

---

## Fixture Usage

```python
# Available fixtures
page: Page                  # Playwright page object
load_test_data             # Test data from JSON

# Use in test
def test_example(page: Page, load_test_data):
    test_data = load_test_data
    username = test_data["username"]
```

---

## Test Data Access

```python
test_data = load_test_data

# Common data fields
test_data["url"]                # Application URL
test_data["username"]           # Test email
test_data["password"]           # Test password
test_data["event_name"]         # Test event
test_data["customer_name"]      # Test customer name
test_data["customer_email"]     # Test customer email
test_data["customer_phone"]     # Test phone
test_data["bookings_url"]       # Bookings page URL
test_data["refund_status"]      # Refund status text
```

---

## Environment Variables

```bash
# Enable debug logging
DEBUG=pw:api pytest

# Playwright debug
PWDEBUG=1 pytest

# Custom browser path
PLAYWRIGHT_BROWSERS_PATH=/custom/path pytest

# Set as CI environment
CI=true pytest
```

---

## Troubleshooting

### Timeout Error
→ Increase timeout or add explicit wait

### Element Not Found
→ Check selector is correct
→ Wait for element: `wait_for(state="visible")`

### Test Isolation Issues
→ Ensure no test dependencies
→ Use fixtures for setup

### Browser Crash
→ Run with `--headed` to see what's happening
→ Check system resources
→ Increase timeout values

### Authentication Issues
→ Verify credentials in `data_setup.json`
→ Check if test account still exists
→ Verify network connectivity

---

## File Naming Conventions

```
Test Files:    test_EventHub_<Feature>_<Scenario>.py
Test Functions: test_<feature>_<scenario>()
Test Classes:   class Test<Feature>:

Examples:
- test_EventHub_Login_valid_credentials.py
- test_login_with_valid_email()
- class TestLoginFunctionality:
```

---

## Best Practices Checklist

- ✅ Use descriptive test names
- ✅ Write clear docstrings
- ✅ Follow AAA pattern (Arrange-Act-Assert)
- ✅ Use load_test_data fixture
- ✅ Add appropriate markers
- ✅ Use Playwright waits (not time.sleep)
- ✅ Keep tests focused and independent
- ✅ No hardcoded values
- ✅ Run tests locally before committing
- ✅ Update documentation

---

## Important Links

- **Project Repo:** [Your Repository]
- **EventHub App:** https://eventhub.rahulshettyacademy.com/
- **Playwright Docs:** https://playwright.dev/python/
- **pytest Docs:** https://docs.pytest.org/
- **Python Docs:** https://docs.python.org/3/

---

## Getting Help

1. Check **[INDEX.md](INDEX.md)** for documentation index
2. Read **[README.md](README.md)** for overview
3. Follow **[SETUP.md](SETUP.md)** for installation
4. Review **[TEST_GUIDE.md](TEST_GUIDE.md)** for test writing
5. See **[ARCHITECTURE.md](ARCHITECTURE.md)** for design
6. Follow **[CONTRIBUTING.md](CONTRIBUTING.md)** for standards

---

## Command Cheat Sheet

```bash
# Essential commands
pip install -e .                    # Install project
pytest                              # Run all tests
pytest -v                           # Verbose output
pytest -s                           # Show prints
pytest --headed                     # See browser
pytest -m smoke                     # Run smoke tests
PWDEBUG=1 pytest -s test_file.py   # Debug mode

# Analysis
pytest --collect-only               # List all tests
pytest --durations=10               # Show slow tests
pytest --html=report.html           # Generate report

# Git commands
git checkout -b feature/name        # Create branch
git commit -m "type: message"       # Commit
git push origin feature/name        # Push
```

---

**Keep This Handy! 📌**

Print or bookmark this page for quick reference while working on tests.

**Last Updated:** August 18, 2026

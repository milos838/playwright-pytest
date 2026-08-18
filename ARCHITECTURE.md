# Project Architecture and Design

## Overview

The EventHub Test Automation project follows modern test automation best practices using Playwright and pytest. This document explains the architecture, design decisions, and structural organization.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Test Execution Layer                    │
│                                                              │
│  pytest Runner  ─────────────────────────────────────────  │
│  (Discovers and                                             │
│   Executes Tests)                                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Configuration Layer                       │
│                                                              │
│  conftest.py          pyproject.toml        .pytest.ini     │
│  ├─ Fixtures         ├─ Dependencies       ├─ Markers       │
│  ├─ Setup/Teardown   ├─ Settings          ├─ Paths         │
│  └─ Browser Config   └─ Versions           └─ Options       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Test Cases Layer                            │
│                                                              │
│  Tests/                                                      │
│  ├─ test_EventHub_Login_*.py                               │
│  ├─ test_EventHub_UI_*.py                                  │
│  ├─ test_EventHub_Bookings_*.py                            │
│  └─ test_EventHub_Events_*.py                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Automation Framework Layer                      │
│                                                              │
│  Playwright (sync_api)                                      │
│  ├─ Page Object                                            │
│  ├─ Browser Automation                                     │
│  ├─ Element Locators                                       │
│  └─ Assertions                                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Browser Layer                              │
│                                                              │
│  Chromium Browser Instance                                  │
│  ├─ Browser Context                                        │
│  ├─ Page                                                   │
│  └─ Network/DOM Interaction                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Application Under Test (AUT)                   │
│                                                              │
│  EventHub - https://eventhub.rahulshettyacademy.com/       │
│  ├─ Login Page                                             │
│  ├─ Events Page                                            │
│  ├─ Bookings Page                                          │
│  └─ Event Details                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

### Root Level Files

```
playwright-pytest/
├── conftest.py                 # pytest configuration and fixtures
├── pyproject.toml              # Project metadata and dependencies
├── README.md                   # Main documentation
├── SETUP.md                    # Setup and installation guide
├── TEST_GUIDE.md               # Test writing guide
├── ARCHITECTURE.md             # This file
├── CONTRIBUTING.md             # Contributing guidelines
└── .gitignore                  # Git ignore rules
```

### Data Directory

```
Data/
└── data_setup.json             # Test data and configuration
    ├── url                     # Application URL
    ├── username                # Test user email
    ├── password                # Test user password
    ├── event_name              # Test event name
    ├── customer_name           # Test customer details
    ├── customer_email          # Test customer email
    ├── customer_phone          # Test customer phone
    └── bookings_url            # URL endpoints
```

**Purpose:** Externalize test data from code for easier maintenance and configuration management.

### Tests Directory

```
Tests/
├── test_EventHub_Login_page_navigation.py
│   └── test_eventHub_login_page_navigation()
│
├── test_EventHub_UI_login_functionality.py
│   └── test_eventhub_ui_login_functionality()
│
├── test_EventHub_UI_Event_booking.py
│   └── test_E2E_book_an_event()
│
├── test_EventHub_Events_options.py
│   └── Test event browsing functionality
│
├── test_EventHub_Bookings_options.py
│   └── Test booking management
│
├── test_EventHub_UI_Cancel_booked_event.py
│   └── Test cancellation workflow
│
└── test_EventHub_UI_View_booked_event_details.py
    └── Test viewing booking details
```

**Naming Convention:** `test_<feature>_<scenario>.py`

**Organization:** Tests are organized by feature/functionality rather than test type.

### Pages Directory (Empty - Ready for Page Object Model)

```
Pages/
├── __init__.py
├── base_page.py               # Base page class
├── login_page.py              # Login page object
├── events_page.py             # Events listing page
├── event_details_page.py       # Event details page
├── booking_page.py            # Booking form page
├── bookings_page.py           # Bookings listing page
└── confirmation_page.py       # Confirmation page
```

**Future Use:** This directory is prepared for implementing Page Object Model pattern for better maintainability.

### Utils Directory (Empty - Ready for Utilities)

```
Utils/
├── __init__.py
├── common_actions.py          # Common UI actions
├── assertions.py              # Custom assertions
├── data_generator.py          # Test data generation
├── logger.py                  # Logging utilities
├── wait_helpers.py            # Wait/timeout helpers
└── file_helpers.py            # File/screenshot utilities
```

**Future Use:** This directory will contain utility functions and helpers for tests.

---

## Design Patterns

### 1. Fixture-Based Setup

**Pattern:** Use pytest fixtures for test setup and data provision.

```python
# conftest.py
@pytest.fixture(scope="session")
def load_test_data():
    """Load test data from JSON file."""
    # Implementation
    
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context."""
    # Implementation
```

**Benefits:**
- Reusable setup code
- Automatic dependency injection
- Clear test dependencies
- Easy teardown

### 2. Data Externalization

**Pattern:** Store test data in external JSON files, not in code.

```python
# Data/data_setup.json
{
    "url": "...",
    "username": "...",
    "password": "..."
}

# In test
test_data = load_test_data
page.locator("#email").fill(test_data["username"])
```

**Benefits:**
- Separation of concerns
- Easy data updates without code changes
- Configuration per environment
- Security (credentials not in source code)

### 3. Arrange-Act-Assert (AAA)

**Pattern:** Structure tests in three clear sections.

```python
def test_login(page, load_test_data):
    # ARRANGE - Setup test state
    test_data = load_test_data
    page.goto(test_data["url"])
    
    # ACT - Perform the action
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    page.locator("#login-btn").click()
    
    # ASSERT - Verify outcome
    expect(page.locator("#user-email-display")).to_have_text(test_data["username"])
```

**Benefits:**
- Clear test structure
- Easy to understand test flow
- Simple to maintain
- Good for documentation

### 4. Test Markers

**Pattern:** Use pytest markers to categorize tests.

```python
@pytest.mark.smoke           # Critical/quick tests
def test_login(page): pass

@pytest.mark.slow            # Long-running tests
def test_complex_workflow(page): pass
```

**Execution:**
```bash
pytest -m smoke              # Run only smoke tests
pytest -m "not slow"         # Run all except slow
```

### 5. Explicit Waits

**Pattern:** Use Playwright's auto-waiting instead of hard sleeps.

```python
# Good - Auto-waits
page.locator("#element").click()

# Avoid - Hard wait
import time
time.sleep(2)

# Explicit wait when needed
page.wait_for_url("expected-url")
page.locator("#element").wait_for(state="visible")
```

---

## Configuration Management

### pytest Configuration (pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]         # Where to find tests
addopts = [                   # Default options
    "--strict-markers",       # Validate markers
    "--strict-config",        # Strict config checking
    "-ra",                    # Show summary
]
markers = [                   # Define markers
    "smoke: quick checks",
    "slow: long-running",
]

[tool.pytest-playwright]
browser = "chromium"          # Browser to use
headed = false                # Headless mode
slow_mo = 0                   # Delay between actions
```

### Pytest Hooks in conftest.py

```python
# Session-scoped fixtures
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context settings."""

# Test-scoped fixtures
@pytest.fixture
def page(page):
    """Customize page fixture."""
    return page

# Fixtures from plugins
@pytest.fixture(scope="session")
def load_test_data():
    """Load external test data."""
```

---

## Test Execution Flow

### 1. Discovery Phase

```
pytest discovers tests matching:
├── Files: test_*.py or *_test.py
├── Classes: Test*
└── Functions: test_*()
```

### 2. Setup Phase

```
For each test:
1. Load fixtures (conftest.py)
   ├── browser_context_args
   └── load_test_data
2. Setup browser context
3. Create page instance
```

### 3. Execution Phase

```
For each test:
1. Setup (Arrange)
2. Actions (Act)
3. Assertions (Assert)
```

### 4. Teardown Phase

```
After each test:
1. Close page
2. Reset browser state
3. Cleanup resources
```

### 5. Reporting Phase

```
Generate results:
├── Console output
├── Exit code (0 = pass, 1 = fail)
├── HTML report (if enabled)
└── Screenshot/video (if enabled)
```

---

## Dependency Tree

```
playwright-pytest/
│
├── External Dependencies
│   ├── playwright >= 1.49.0
│   │   └── Provides browser automation API
│   │
│   ├── pytest >= 8.0.0
│   │   └── Provides test framework
│   │
│   └── pytest-playwright >= 0.6.0
│       └── Provides pytest integration with Playwright
│
├── Internal Configuration
│   ├── conftest.py
│   │   ├── Defines fixtures
│   │   ├── Browser context settings
│   │   └── Test data loading
│   │
│   ├── pyproject.toml
│   │   ├── Project metadata
│   │   ├── Dependency specifications
│   │   └── Tool configurations
│   │
│   └── Data/
│       └── data_setup.json (Test configuration)
│
└── Test Cases
    ├── Depend on: fixtures (page, load_test_data)
    ├── Use: Playwright API
    └── Verify: EventHub application
```

---

## Future Architecture Enhancements

### 1. Page Object Model Implementation

Currently, tests directly interact with Playwright API. Implement POM for better maintainability:

```python
# Pages/login_page.py
class LoginPage:
    def __init__(self, page):
        self.page = page
    
    def login(self, username, password):
        """Encapsulate login interaction."""

# Tests/test_login.py
def test_login(page, load_test_data):
    login_page = LoginPage(page)
    login_page.login(...)
```

### 2. Utility Classes

Create helper classes for common operations:

```python
# Utils/waiter.py
class WaitHelper:
    @staticmethod
    def wait_for_element_visible(page, selector):
        """Wait for element visibility."""

# Utils/data_generator.py
class DataGenerator:
    @staticmethod
    def generate_user_data():
        """Generate random user data."""
```

### 3. Test Parallelization

Use pytest-xdist for parallel execution:

```bash
pytest -n auto  # Run on all CPU cores
```

### 4. CI/CD Integration

Implement continuous integration:
- GitHub Actions
- Test reporting
- Cross-browser testing
- Performance benchmarks

### 5. API Testing Integration

Combine with API testing for comprehensive coverage:
- API setup via tests
- API verification
- End-to-end workflows combining UI + API

### 6. Visual Regression Testing

Add visual testing for UI consistency:
- Screenshot comparison
- Visual diff reporting
- Baseline image management

### 7. Performance Testing

Add performance metrics:
- Page load time
- Response time tracking
- Performance assertions

---

## Best Practices Implemented

✅ **Fixtures for Setup:** Tests use pytest fixtures for configuration  
✅ **Data Externalization:** Test data in JSON, not hardcoded  
✅ **Clear Naming:** Test files and functions clearly named  
✅ **Markers:** Tests marked by type (smoke, slow)  
✅ **Assertion Library:** Playwright's expect() for assertions  
✅ **Page Object Ready:** Pages directory prepared for POM  
✅ **Configuration File:** pyproject.toml for settings  
✅ **Documentation:** Comprehensive setup and test guides  

---

## Technology Decisions

### Why Playwright?

- **Modern:** Supports latest browser features
- **Reliable:** Built-in waiting and auto-waits
- **Fast:** Direct browser protocol communication
- **Cross-Browser:** Works across Chrome, Firefox, Safari
- **Developer Experience:** Easy API and debugging tools

### Why pytest?

- **Powerful:** Fixtures, markers, plugins
- **Extensible:** Large plugin ecosystem
- **Simple:** Easy to write and read tests
- **Compatible:** Works well with Playwright
- **Popular:** Industry standard

### Why JSON for Test Data?

- **Simple:** Easy to read and understand
- **Flexible:** Easy to add more data
- **Standard:** Language-independent
- **Secure:** Keep credentials separate from code

### Why Session Scope for Fixtures?

- **Performance:** Browser and data loaded once per session
- **Isolation:** Each test gets fresh page within session
- **Efficiency:** Reuse browser context across tests

---

## Performance Considerations

### Test Execution Time

Current test execution is optimized for:
- **Fast execution:** ~5-10 seconds per test
- **Headless mode:** Default for CI/CD
- **Parallel execution:** Ready for pytest-xdist

### Browser Resource Usage

- **Single browser instance:** Reused across tests
- **Isolated contexts:** Each test gets its own page
- **Automatic cleanup:** Resources released after tests

### Network Optimization

- **No artificial waits:** Uses Playwright's auto-waiting
- **Timeout-based:** Waits for element/navigation events
- **Network idle:** Can wait for network stabilization

---

## Security Considerations

### Credential Management

✅ **Credentials in data_setup.json (externalized)**  
❌ Never commit real credentials  
✅ Use environment variables for sensitive data  

### Example with Environment Variables

```python
import os
from pathlib import Path
import json

@pytest.fixture(scope="session")
def load_test_data():
    """Load test data with environment override."""
    data_path = Path(__file__).parent / "Data/data_setup.json"
    with open(data_path) as f:
        data = json.load(f)
    
    # Override with environment variables
    data["username"] = os.getenv("TEST_USERNAME", data["username"])
    data["password"] = os.getenv("TEST_PASSWORD", data["password"])
    
    return data
```

---

## Maintenance Guide

### Adding New Tests

1. Create file in `Tests/` following naming convention
2. Import required modules (pytest, Page, expect)
3. Add @pytest.mark for test type
4. Write test following AAA pattern
5. Use `load_test_data` fixture for data
6. Update documentation

### Modifying Test Data

1. Update `Data/data_setup.json`
2. No code changes needed
3. All tests using that data automatically updated

### Debugging Tests

1. Use `PWDEBUG=1` for Playwright Inspector
2. Add print statements (use `-s` flag)
3. Use pdb for step-by-step debugging
4. Capture screenshots/videos for failed tests

### Running Tests in Different Environments

```bash
# Development
pytest --headed -v

# CI/CD
pytest -m smoke --junit-xml=results.xml

# Performance testing
pytest --durations=10

# Full coverage
pytest --cov=Tests --cov-report=html
```

---

## Conclusion

The EventHub Test Automation project demonstrates modern test automation best practices with:

- **Clear architecture:** Layered, well-organized structure
- **Maintainable design:** Using fixtures, external data, markers
- **Scalable framework:** Ready for Page Object Model, utilities
- **Professional standards:** Documentation, configuration, security
- **Future-ready:** Prepared for CI/CD, parallel execution, enhancements

This foundation provides a solid base for expanding test coverage and implementing advanced testing strategies.

---

**Last Updated:** August 18, 2026  
**Architecture Version:** 1.0  
**Framework:** Playwright + pytest

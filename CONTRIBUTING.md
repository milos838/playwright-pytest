# Contributing Guidelines

Thank you for contributing to the EventHub Test Automation project! This document outlines the guidelines and best practices for contributing tests, improvements, and documentation.

## Table of Contents

- [Getting Started](#getting-started)
- [Code of Conduct](#code-of-conduct)
- [Development Workflow](#development-workflow)
- [Writing Tests](#writing-tests)
- [Code Style](#code-style)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)
- [Reporting Issues](#reporting-issues)
- [Documentation](#documentation)

---

## Getting Started

### Prerequisites

1. **Python 3.10+** installed
2. **Git** installed
3. Familiarity with Playwright and pytest
4. Read the [README.md](README.md) and [SETUP.md](SETUP.md)

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd playwright-pytest

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -e .

# Install browsers
playwright install chromium

# Verify setup
pytest -v
```

---

## Code of Conduct

### Be Respectful

- Treat all contributors with respect
- Be open to feedback and different perspectives
- Help others learn and grow

### Be Professional

- Use clear, professional language
- Provide constructive feedback
- Focus on code, not the person

### Be Collaborative

- Help others debug issues
- Share knowledge and experience
- Celebrate successes together

---

## Development Workflow

### 1. Create Feature Branch

Always create a new branch for your work:

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/add-new-test
# Or for bug fixes
git checkout -b fix/login-timeout-issue
```

### 2. Make Changes

```bash
# Make your changes
# Edit files, add tests, update documentation

# Run tests locally
pytest -v

# Check specific test file
pytest Tests/test_file.py -v
```

### 3. Commit Changes

```bash
# Stage changes
git add .

# Commit with clear message (see Commit Messages section)
git commit -m "Add test for event booking with multiple events"
```

### 4. Push to Remote

```bash
# Push your branch
git push origin feature/add-new-test
```

### 5. Create Pull Request

Create a pull request on GitHub with:
- Clear description of changes
- Link to related issue (if applicable)
- List of changes made

### 6. Code Review

- Address review comments
- Run tests again
- Update code as requested
- Re-request review when ready

### 7. Merge

Once approved:
- Ensure all tests pass
- Merge to main branch
- Delete feature branch

---

## Writing Tests

### Test File Structure

```python
"""
Module: test_EventHub_[Feature]_[Scenario].py

Description:
Tests for [feature description].

Test Cases:
- test_[scenario_name]: [scenario description]
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_scenario_name(page: Page, load_test_data):
    """
    Test: [What is being tested].
    
    Scenario:
    1. [Step 1]
    2. [Step 2]
    3. [Step 3]
    
    Expected Result:
    [What should happen]
    """
    # Test implementation
    pass
```

### Naming Convention

**File Names:**
```
test_EventHub_[Feature]_[Scenario].py

Examples:
- test_EventHub_Login_valid_credentials.py
- test_EventHub_Login_invalid_password.py
- test_EventHub_Bookings_cancel_refund.py
- test_EventHub_Events_filter_by_category.py
```

**Function Names:**
```
test_[feature]_[scenario]

Examples:
- test_login_with_valid_credentials()
- test_login_with_invalid_email()
- test_book_event_complete_workflow()
- test_cancel_booking_verify_refund()
```

### Test Requirements

✅ **Required:**
1. Clear, descriptive function name
2. Comprehensive docstring
3. Appropriate pytest marker (@pytest.mark.smoke, etc.)
4. Setup-Action-Assert structure (AAA)
5. Use load_test_data fixture for data
6. Use page fixture from Playwright
7. Proper assertions using expect()

✅ **Recommended:**
1. Single focused scenario
2. Independent (no dependencies on other tests)
3. Fast execution (< 30 seconds)
4. Clear assertions with meaningful messages
5. Comment for complex logic

❌ **Avoid:**
1. Hard waits (time.sleep)
2. Multiple unrelated scenarios in one test
3. Hardcoded values
4. Brittle locators
5. Long test names
6. Duplicate test code

### Example Test

```python
"""
Module: test_EventHub_Bookings_cancel.py

Tests for booking cancellation functionality.
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_cancel_booking_and_verify_refund_eligibility(page: Page, load_test_data):
    """
    Test: User can cancel a booking and see refund status.
    
    Scenario:
    1. Login with valid credentials
    2. Navigate to bookings
    3. Find and select a booked event
    4. Click cancel booking button
    5. Confirm cancellation
    
    Expected Result:
    - Booking is cancelled
    - Refund eligibility status is displayed
    """
    test_data = load_test_data
    
    # SETUP - Navigate and login
    page.goto(test_data["url"])
    page.locator("#email").fill(test_data["username"])
    page.locator("#password").fill(test_data["password"])
    page.locator("#login-btn").click()
    
    # ACTION - Navigate to bookings and cancel
    page.goto(test_data["bookings_url"])
    page.wait_for_url(test_data["bookings_url"])
    
    # Find the booking to cancel
    booking = page.locator(".booking-card").first
    page.locator(".cancel-booking-btn").click()
    
    # Confirm cancellation
    page.locator("#confirm-cancel").click()
    
    # ASSERT - Verify cancellation and refund status
    expect(page.locator(".success-message")).to_contain_text("Booking cancelled")
    expect(page.locator(".refund-status")).to_contain_text(test_data["refund_status"])
```

---

## Code Style

### Python Style Guide

We follow PEP 8 with these additions:

### Imports

```python
# Good - Organized imports
import pytest
from pathlib import Path
from playwright.sync_api import Page, expect

# Bad - Random order
from playwright.sync_api import expect, Page
import pytest
from pathlib import Path
```

### Naming

```python
# Good - Clear, descriptive names
def test_login_with_valid_credentials(page, load_test_data):
    user_email = load_test_data["username"]
    login_button = page.locator("#login-btn")

# Bad - Vague names
def test_login(page, data):
    e = data["u"]
    b = page.locator("button")
```

### Line Length

Keep lines under 100 characters:

```python
# Good
page.locator("#customer-email").fill(test_data["customer_email"])

# Bad - Too long
very_long_variable_name = page.locator("#customer-email-input-field").fill(test_data["customer_email_address"])
```

### Comments

```python
# Good - Explains why, not what
# Wait for background job to complete before verification
page.wait_for_load_state("networkidle")

# Bad - Explains what (already obvious)
# Fill the email field
page.locator("#email").fill(email)
```

### Type Hints

Use type hints for clarity:

```python
# Good
def test_login(page: Page, load_test_data: dict) -> None:
    pass

# Bad
def test_login(page, load_test_data):
    pass
```

---

## Commit Messages

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat:** New feature or test
- **fix:** Bug fix or issue resolution
- **test:** Test improvements or new tests
- **docs:** Documentation changes
- **refactor:** Code refactoring
- **style:** Code style changes
- **chore:** Dependency updates, setup changes

### Scope

- **login:** Login-related changes
- **booking:** Booking-related changes
- **events:** Events-related changes
- **ui:** UI interaction changes
- **fixtures:** Fixture changes
- **config:** Configuration changes

### Examples

**Good Commit Messages:**

```
feat(booking): Add test for multiple event booking workflow

- Added test for booking multiple events in sequence
- Added test data for multiple events
- Verified booking confirmation for each event

Closes #123
```

```
fix(login): Resolve timeout issue on slow networks

- Increased wait timeout from 5s to 10s
- Added networkidle wait state
- Added test for slow network scenario

Closes #456
```

```
test(events): Add tests for event filtering

- Add test for filtering events by category
- Add test for filtering events by date
- Add test for filtering events by price range
```

```
docs: Update test writing guidelines

- Add examples for data-driven tests
- Add debugging tips
- Clarify naming conventions
```

**Bad Commit Messages:**

```
updated files              # Too vague
fix bug                    # No context
test                       # No description
Added new test lol         # Unprofessional
```

---

## Pull Requests

### Before Creating a PR

1. ✅ Run all tests locally: `pytest -v`
2. ✅ Run linter if configured
3. ✅ Update documentation if needed
4. ✅ Check for console errors and warnings
5. ✅ Rebase on latest main branch
6. ✅ Review your own changes first

### PR Title Format

```
[Type] Description of changes

Examples:
- [Feature] Add tests for event filtering
- [Fix] Resolve login timeout on slow networks
- [Docs] Update test writing guide
```

### PR Description Template

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] New test
- [ ] Bug fix
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Other (please describe)

## Related Issue
Closes #123

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing Done
- Ran test suite: `pytest -v`
- Ran specific tests: `pytest Tests/test_file.py`
- All tests passing: Yes/No

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Added docstrings to new tests
- [ ] Updated documentation
- [ ] No breaking changes
- [ ] All tests pass
```

### During Review

- Respond promptly to feedback
- Ask clarifying questions if needed
- Make requested changes
- Re-request review when updated
- Be open to suggestions

### After Approval

- Wait for CI/CD to pass
- Ensure all commits are clean
- Merge to main
- Delete feature branch

---

## Reporting Issues

### Issue Title Format

```
[Component] Brief description of issue

Examples:
- [Login] Timeout error on slow networks
- [Booking] Cancel button not working
- [Setup] Installation fails on Windows
```

### Issue Description Template

```markdown
## Description
Clear description of the issue.

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- OS: Windows/macOS/Linux
- Python: 3.10/3.11/3.12
- Playwright: 1.49.0
- pytest: 8.0.0

## Screenshots/Logs
[If applicable, add screenshots or error logs]

## Additional Context
[Any other relevant information]
```

---

## Documentation

### Update README.md

If your changes affect:
- Installation process → Update SETUP.md
- Test execution → Update TEST_GUIDE.md
- Project structure → Update ARCHITECTURE.md
- Contribution process → Update CONTRIBUTING.md
- Project overview → Update README.md

### Documentation Style

- Use clear, simple language
- Include examples
- Add code blocks for technical content
- Use proper Markdown formatting
- Keep documentation up-to-date

### Documentation Checklist

- [ ] Updated relevant documentation files
- [ ] Added examples if introducing new patterns
- [ ] Verified links work correctly
- [ ] Checked spelling and grammar
- [ ] Followed Markdown style guide

---

## Testing Your Changes

### Run Full Test Suite

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest Tests/test_EventHub_UI_login_functionality.py -v
```

### Run Smoke Tests Only

```bash
pytest -m smoke -v
```

### Run with Coverage

```bash
pip install pytest-cov
pytest --cov=Tests --cov-report=html
```

### Run in Headed Mode (Debug)

```bash
pytest --headed -v
```

### Run with Debug Output

```bash
PWDEBUG=1 pytest -s Tests/test_file.py
```

---

## Code Review Checklist

When reviewing code:

- [ ] Does it follow the naming convention?
- [ ] Does it follow the code style?
- [ ] Are there comprehensive docstrings?
- [ ] Is it using the AAA pattern?
- [ ] Is it using load_test_data fixture?
- [ ] Are assertions clear and meaningful?
- [ ] Are there no hard waits (time.sleep)?
- [ ] Is it independent and focused?
- [ ] Does it pass all tests?
- [ ] Is documentation updated?

---

## Common Scenarios

### Adding a New Test

1. Create file: `Tests/test_EventHub_[Feature]_[Scenario].py`
2. Write test following template
3. Use load_test_data for test data
4. Add appropriate marker (@pytest.mark.smoke)
5. Run test: `pytest Tests/test_file.py -v`
6. Update TEST_GUIDE.md if needed
7. Create pull request

### Fixing a Failing Test

1. Identify root cause
2. Check if application changed
3. Update selectors if needed
4. Add explicit waits if timing issue
5. Increase timeout if needed
6. Add debugging output for complex tests
7. Run test multiple times to verify
8. Document change in commit message

### Updating Test Data

1. Edit `Data/data_setup.json`
2. No code changes needed
3. Run tests to verify
4. Tests automatically use new data

### Adding a New Feature Test

1. Understand the feature
2. Plan test scenarios
3. Create test file
4. Implement test
5. Run locally
6. Update documentation
7. Create pull request

---

## Performance Tips

### Write Fast Tests

- Avoid unnecessary waits
- Use Playwright's auto-waiting
- Focus on critical paths
- Keep tests focused and small

### Optimize Test Execution

```bash
# Run tests in parallel
pip install pytest-xdist
pytest -n auto

# Run only smoke tests for quick feedback
pytest -m smoke

# Run failed tests from last run
pytest --lf
```

---

## Getting Help

- Check existing documentation: README.md, SETUP.md, TEST_GUIDE.md
- Review ARCHITECTURE.md for patterns
- Look at existing tests for examples
- Check Playwright documentation: https://playwright.dev/python/
- Check pytest documentation: https://docs.pytest.org/

---

## Recognition

All contributors are recognized for their work. Thank you for helping improve the EventHub Test Automation project!

---

**Last Updated:** August 18, 2026  
**Contribution Guidelines Version:** 1.0

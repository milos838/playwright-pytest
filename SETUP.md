# Setup and Installation Guide

## Quick Start (5 minutes)

### Windows
```bash
# 1. Clone repository
git clone <repository-url>
cd playwright-pytest

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -e .

# 4. Install browsers
playwright install chromium

# 5. Run tests
pytest
```

### macOS/Linux
```bash
# 1. Clone repository
git clone <repository-url>
cd playwright-pytest

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -e .

# 4. Install browsers
playwright install chromium

# 5. Run tests
pytest
```

---

## Detailed Installation Steps

### Step 1: System Requirements

Verify your system meets these requirements:

**Windows:**
```powershell
python --version        # Should be >= 3.10
pip --version          # Should be present
```

**macOS:**
```bash
python3 --version      # Should be >= 3.10
pip3 --version         # Should be present
```

**Linux (Ubuntu/Debian):**
```bash
python3 --version      # Should be >= 3.10
pip3 --version         # Should be present
# May need: sudo apt-get install python3-venv python3-pip
```

### Step 2: Download and Navigate to Project

```bash
git clone <repository-url>
cd playwright-pytest
```

### Step 3: Create Virtual Environment

A virtual environment isolates project dependencies from your system Python.

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Verify activation** (you should see `(.venv)` in your terminal):
```bash
which python  # macOS/Linux
where python  # Windows
```

### Step 4: Upgrade pip (Optional but Recommended)

```bash
python -m pip install --upgrade pip
```

### Step 5: Install Project Dependencies

The project uses `pyproject.toml` for configuration. Install all dependencies:

```bash
pip install -e .
```

This installs:
- `playwright>=1.49.0` - Browser automation engine
- `pytest>=8.0.0` - Test framework
- `pytest-playwright>=0.6.0` - pytest plugin for Playwright

**Verify installation:**
```bash
pip list
```

You should see:
```
playwright
pytest
pytest-playwright
```

### Step 6: Install Playwright Browsers

Playwright requires browser binaries to be installed:

```bash
# Install only Chromium (recommended for this project)
playwright install chromium

# Or install all browsers
playwright install

# Verify installation
playwright install --with-deps  # Includes system dependencies
```

This downloads:
- Chromium binary (~200MB)
- WebKit binary (if installing all)
- Firefox binary (if installing all)

**Note:** On Linux, you may need to install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install libgbm1 libx11-6

# Fedora
sudo dnf install libgbm libxcb

# Or let Playwright handle it:
playwright install --with-deps chromium
```

### Step 7: Verify Installation

Create a simple test file to verify everything works:

**verify_setup.py:**
```python
from playwright.sync_api import sync_playwright

def test_playwright_works():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://example.com")
        assert page.title() == "Example Domain"
        browser.close()

if __name__ == "__main__":
    test_playwright_works()
    print("✓ Playwright setup verified!")
```

Run it:
```bash
python verify_setup.py
```

### Step 8: Run Sample Test

```bash
pytest Tests/test_EventHub_Login_page_navigation.py -v
```

**Expected output:**
```
test_EventHub_Login_page_navigation.py::test_eventHub_login_page_navigation PASSED [100%]
1 passed in X.XXs
```

---

## Configuration

### Project Configuration (pyproject.toml)

The project configuration controls:

```toml
[project]
name = "playwright-pytest"              # Project name
version = "0.1.0"                       # Version number
description = "Playwright end-to-end tests with pytest"
requires-python = ">=3.10"              # Python version requirement
dependencies = [                        # Required packages
    "playwright>=1.49.0",
    "pytest>=8.0.0",
    "pytest-playwright>=0.6.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]                   # Where to find tests
addopts = [                             # Default pytest options
    "--strict-markers",                 # Only use defined markers
    "--strict-config",                  # Strict configuration
    "-ra",                              # Show summary of all tests
]
markers = [                             # Define custom markers
    "smoke: quick sanity checks",
    "slow: tests that take longer to run",
]

[tool.pytest-playwright]
browser = "chromium"                    # Browser to use
headed = false                          # Headless mode (true = see browser)
slow_mo = 0                             # Delay between actions (ms)
```

### Customize Configuration

**Change browser to Firefox:**
```toml
[tool.pytest-playwright]
browser = "firefox"
```

**Run tests in headed mode (see browser):**
```bash
pytest --headed
```

Or update `pyproject.toml`:
```toml
[tool.pytest-playwright]
headed = true
```

**Add delay between actions (useful for debugging):**
```bash
pytest --slowmo=1000  # 1 second delay
```

Or in `pyproject.toml`:
```toml
[tool.pytest-playwright]
slow_mo = 1000
```

### Browser Context Configuration (conftest.py)

Modify `conftest.py` to customize browser context:

```python
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Customize browser context for all tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},  # Change viewport
        "locale": "en-GB",                             # Change locale
        "timezone_id": "Europe/London",                # Change timezone
        "permissions": ["geolocation"],                # Add permissions
        "geolocation": {"latitude": 51.5074, "longitude": -0.1278},
    }
```

---

## Environment Variables

Set up environment variables for configuration:

**Windows (PowerShell):**
```powershell
$env:PLAYWRIGHT_BROWSERS_PATH = "C:\path\to\browsers"
$env:DEBUG = "pw:api"
```

**Windows (Command Prompt):**
```cmd
set PLAYWRIGHT_BROWSERS_PATH=C:\path\to\browsers
set DEBUG=pw:api
```

**macOS/Linux:**
```bash
export PLAYWRIGHT_BROWSERS_PATH=/path/to/browsers
export DEBUG=pw:api
```

### Common Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `PLAYWRIGHT_BROWSERS_PATH` | Custom browser install location | `/custom/path` |
| `DEBUG` | Enable debug logging | `pw:api` |
| `PWDEBUG` | Launch Playwright Inspector | `1` |
| `CI` | Mark as CI environment | `true` |

---

## Troubleshooting Installation

### Python Not Found
```
Error: Python is not installed or not in PATH
```

**Solution:**
1. Download Python 3.10+ from [python.org](https://www.python.org/)
2. During installation, check "Add Python to PATH"
3. Restart terminal after installation
4. Verify: `python --version`

### Virtual Environment Issues

**Virtual environment not activating:**
```bash
# Windows - Try batch file instead of PS1
.venv\Scripts\activate.bat

# macOS/Linux - Ensure correct shell
source .venv/bin/activate
```

**Remove and recreate virtual environment:**
```bash
# Remove existing
rm -rf .venv  # macOS/Linux
rmdir /s .venv  # Windows

# Create new
python -m venv .venv
```

### pip Install Fails

**Issue: SSL certificate error**
```bash
pip install --trusted-host pypi.python.org -e .
```

**Issue: No module named 'pip'**
```bash
python -m ensurepip --default-pip
```

**Issue: Permission denied**
```bash
# Don't use sudo with pip
pip install --user -e .
```

### Playwright Browser Installation Fails

**Issue: Insufficient disk space**
```
The browser binaries require ~500MB total space
```

**Issue: Network timeout downloading browsers**
```bash
# Retry download
playwright install --with-deps chromium

# Or use alternative mirror (for China):
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright
playwright install chromium
```

**Issue: System dependencies missing (Linux)**
```bash
# Ubuntu/Debian
sudo apt-get install -y libgbm1 libx11-6 libxss1

# Fedora
sudo dnf install -y libgbm libxcb

# Or let Playwright install them
playwright install --with-deps chromium
```

### Test Execution Fails

**Issue: Port already in use**
- Close other Playwright instances
- Use different port: `pytest --port=8001`

**Issue: Browser crashes during test**
```bash
# Run with less performance but more stability
pytest --headed  # See what's happening
pytest -s  # Show print statements
```

**Issue: Test timeouts**
```python
# Increase timeout in conftest.py
@pytest.fixture
def page(page):
    page.set_default_timeout(30000)  # 30 seconds
    return page
```

---

## Advanced Setup

### Running Tests in Docker

**Dockerfile:**
```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

WORKDIR /app

COPY . .

RUN pip install -e .

CMD ["pytest"]
```

**Build and run:**
```bash
docker build -t eventhub-tests .
docker run eventhub-tests
```

### Running Tests in CI/CD

**GitHub Actions:**
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -e .
    playwright install chromium

- name: Run tests
  run: pytest -m smoke
```

**GitLab CI:**
```yaml
test:
  image: mcr.microsoft.com/playwright/python:v1.49.0-jammy
  script:
    - pip install -e .
    - pytest -m smoke
```

---

## Verifying Full Setup

Run this complete verification:

```bash
# 1. Check Python version
python --version

# 2. Check pip packages
pip list | grep -E "playwright|pytest"

# 3. Check playwright browsers
playwright install --with-deps chromium

# 4. Run basic test
pytest Tests/test_EventHub_Login_page_navigation.py -v

# 5. Check all tests can be discovered
pytest --collect-only

# 6. Run smoke tests
pytest -m smoke -v
```

All should complete without errors.

---

## Next Steps

After successful setup:

1. Read [README.md](README.md) for project overview
2. Review [TEST_GUIDE.md](TEST_GUIDE.md) to write new tests
3. Check [ARCHITECTURE.md](ARCHITECTURE.md) for project structure
4. Explore [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
5. Run your first test: `pytest Tests/ -v`

---

## Getting Help

- **Playwright Docs:** https://playwright.dev/python/
- **pytest Docs:** https://docs.pytest.org/
- **Python Docs:** https://docs.python.org/3/
- **EventHub:** https://eventhub.rahulshettyacademy.com/

---

**Setup Version:** 1.0  
**Last Updated:** August 18, 2026

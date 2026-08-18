# GitHub Actions Setup Guide

## Overview

GitHub Actions provides free CI/CD automation for your repository. This guide explains the EventHub test automation workflows and how to use them.

## What is GitHub Actions?

GitHub Actions is an automation platform that runs workflows triggered by GitHub events. For this project, workflows automatically:
- Run tests on every push
- Run tests on pull requests
- Generate test reports and coverage
- Test across multiple Python versions and browsers
- Run scheduled tests

## Workflows Included

### 1. Main Test Workflow (test.yml)

**When it runs:**
- On every push to main or develop branches
- On every pull request to main or develop branches

**What it does:**
- Runs tests on Python 3.10, 3.11, and 3.12
- Runs smoke tests (quick sanity check)
- Runs full test suite
- Performs code quality checks
- Generates HTML test reports
- Uploads reports as artifacts

**Test Matrix:**
```
Python 3.10 → Full test suite → HTML report
Python 3.11 → Full test suite → HTML report
Python 3.12 → Full test suite → HTML report
```

**View Results:**
1. Push or create PR
2. Go to "Actions" tab on GitHub
3. Click workflow run
4. See detailed logs
5. Download "Artifacts" section for test reports

### 2. Code Coverage Workflow (coverage.yml)

**When it runs:**
- On every push to main or develop
- On every pull request
- Daily at 2 AM UTC
- Manual trigger available

**What it does:**
- Generates test coverage report
- Uploads coverage to Codecov
- Comments on PRs with coverage percentage
- Saves coverage reports as artifacts

**Outputs:**
- XML coverage report
- HTML coverage report
- Codecov integration

**View Coverage:**
1. Check PR comments for coverage change
2. Go to "Actions" tab → Coverage workflow
3. Download coverage-report artifact
4. Open htmlcov/index.html in browser

### 3. Cross-Browser Testing (cross-browser.yml)

**When it runs:**
- Every Monday and Friday at 6 AM UTC
- Manual trigger available

**What it does:**
- Tests on Chromium browser
- Tests on Firefox browser
- Tests on WebKit browser
- Generates browser-specific reports

**Browsers Tested:**
- Chromium (default)
- Firefox
- WebKit (Safari)

**Use Cases:**
- Ensure compatibility across browsers
- Catch browser-specific issues
- Regular regression testing

## File Structure

```
.github/
└── workflows/
    ├── README.md                 # This documentation
    ├── test.yml                  # Main test workflow
    ├── coverage.yml              # Coverage analysis
    └── cross-browser.yml         # Cross-browser tests
```

## Workflow Triggers Explained

### Push Trigger
```yaml
on:
  push:
    branches: [ main, develop ]
```

Runs when you push code to main or develop branches.

### Pull Request Trigger
```yaml
on:
  pull_request:
    branches: [ main, develop ]
```

Runs when a PR is created or updated for main or develop branches.

### Scheduled Trigger
```yaml
schedule:
  - cron: '0 2 * * *'  # Daily at 2 AM UTC
```

Runs automatically at specified times (cron format).

### Manual Trigger
```yaml
on:
  workflow_dispatch:
```

Allows running workflow manually from GitHub UI.

## Understanding Cron Syntax

Cron expressions control scheduled workflow timing:

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (0 = Sunday)
│ │ │ │ │
│ │ │ │ │
* * * * *
```

Examples:
```yaml
'0 2 * * *'      # Daily at 2:00 AM UTC
'0 0 * * MON'    # Every Monday at midnight UTC
'0 6 * * 1,5'    # Every Monday and Friday at 6 AM UTC
'0 */6 * * *'    # Every 6 hours
'0 0 * * 0'      # Every Sunday at midnight
```

## Viewing Workflow Runs

### On GitHub Website

1. **Go to Actions tab**
   - Click "Actions" in repository menu

2. **Select workflow**
   - Click workflow name (Playwright Tests, Coverage, etc.)

3. **View run details**
   - Click specific run
   - See logs for each job/step
   - Download artifacts

4. **Check status badge**
   - Shows green ✅ if passed
   - Shows red ❌ if failed
   - Shows yellow ⚠️ if in progress

### Checking Test Results

For each workflow run:
- **Logs**: Real-time test execution output
- **Artifacts**: Generated reports (HTML, coverage, etc.)
- **Annotations**: Highlighted errors and warnings

### Downloading Artifacts

1. Go to workflow run
2. Scroll to "Artifacts" section
3. Click download (zip file)
4. Extract and view reports locally

## Environment Variables in Workflows

Workflows can access:

```yaml
# GitHub provided
${{ github.event_name }}      # Trigger type (push, pull_request)
${{ github.ref }}             # Branch reference
${{ github.repository }}      # Repository name
${{ matrix.python-version }}  # Current Python version in matrix

# Custom
${{ secrets.GITHUB_TOKEN }}   # Provided by GitHub
```

## Modifying Workflows

### Add New Job

```yaml
jobs:
  my-new-job:
    name: My New Job
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      - run: echo "Hello, World!"
```

### Change Branches

```yaml
on:
  push:
    branches: [ main, develop, staging ]
  pull_request:
    branches: [ main, develop, staging ]
```

### Add Python Version

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']  # Add version here
```

### Change Schedule

```yaml
schedule:
  - cron: '0 2 * * *'  # Change time here
```

### Add Step

```yaml
steps:
  - name: My custom step
    run: |
      echo "Running custom command"
      pytest -v
```

## Common Workflow Patterns

### Skip Tests for Documentation Changes

```yaml
on:
  push:
    branches: [ main ]
    paths-ignore:
      - '**.md'           # Skip if only .md files changed
      - '.github/ISSUE_*'
```

### Run Only on PR

```yaml
on:
  pull_request:
    types:
      - opened
      - synchronize
```

### Run with Custom Python Version

```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.11'
```

### Conditional Steps

```yaml
- name: Upload report
  if: always()  # Run even if previous step failed
  uses: actions/upload-artifact@v3
```

### Continue on Error

```yaml
- name: Run risky step
  run: might-fail-command
  continue-on-error: true  # Don't stop workflow if this fails
```

## Debugging Workflows

### View Logs

1. Go to Actions
2. Click failing workflow run
3. Click failing job
4. Expand failed step to see error

### Enable Debug Logging

```yaml
- name: Enable debug
  run: |
    export ACTIONS_STEP_DEBUG=true
```

### Add Debug Output

```yaml
- name: Debug info
  run: |
    echo "Current branch: ${{ github.ref }}"
    echo "Python version: ${{ matrix.python-version }}"
    echo "Event: ${{ github.event_name }}"
```

### Common Issues

**Tests timeout**
- Increase timeout value
- Run smoke tests only
- Check for hanging processes

**Dependency installation fails**
- Clear cache: Re-run workflow with cache cleared
- Check Python version compatibility
- Verify pip is up to date

**Browser crashes**
- Increase memory
- Use headless mode (default)
- Install system dependencies

**Artifact too large**
- Reduce retention days
- Don't save all screenshots
- Clean up after tests

## Adding Status Badge to README

Display workflow status in README.md:

```markdown
# EventHub Test Automation

![Tests](https://github.com/milos838/playwright-pytest/workflows/Playwright%20Tests/badge.svg)
![Coverage](https://codecov.io/gh/milos838/playwright-pytest/branch/main/graph/badge.svg)
```

## Performance Tips

### Optimize Workflow Speed

1. **Cache dependencies**
   ```yaml
   cache: 'pip'  # Cache pip packages
   ```

2. **Run parallel jobs**
   ```yaml
   strategy:
     matrix:
       python-version: ['3.10', '3.11', '3.12']
   ```

3. **Fail fast option**
   ```yaml
   strategy:
     fail-fast: true  # Stop other tests if one fails
   ```

4. **Limit test matrix**
   - Test on latest Python for PRs
   - Test on all versions before merge

5. **Use smaller test sets**
   ```yaml
   pytest -m smoke  # Quick smoke tests
   ```

## Security Considerations

### Secrets Management

Never store sensitive data in workflows:

```yaml
# ❌ DON'T - Exposes password
- run: pytest --password=mypassword

# ✅ DO - Use GitHub Secrets
- run: pytest --password=${{ secrets.TEST_PASSWORD }}
```

### Add Secrets

1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add name and value
4. Use in workflow: `${{ secrets.SECRET_NAME }}`

### Protect Workflows

```yaml
permissions:
  contents: read
  checks: write
```

## Scheduled Runs

### Why Schedule Tests?

- Regular regression testing
- Monitor application stability
- Catch intermittent failures
- Test at low-traffic times
- Generate periodic reports

### Setting Up Scheduled Runs

Use cron syntax:
```yaml
schedule:
  - cron: '0 2 * * *'  # Daily at 2 AM UTC
  - cron: '0 6 * * 1,5'  # Monday & Friday at 6 AM
```

### Monitoring Scheduled Runs

1. Go to Actions
2. Click "Scheduled runs"
3. View results and logs
4. Check for failures
5. Download reports

## Integration with Pull Requests

Workflows automatically:
- Run on PR creation/update
- Show status check on PR
- Block merge if tests fail (if configured)
- Comment with results

### Require Status Checks

1. Go to Settings
2. Click Branches
3. Add branch protection rule
4. Require status checks to pass
5. Select workflow checks

## Next Steps

1. **Commit workflow files** to `.github/workflows/`
2. **Push to GitHub** and watch Actions tab
3. **Create a pull request** to test the workflow
4. **Review results** in Actions tab
5. **Fix any issues** and re-run workflow

## Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)
- [Playwright CI Guide](https://playwright.dev/python/docs/ci)
- [Codecov Documentation](https://docs.codecov.com/)

## Troubleshooting

### Workflow doesn't run
- Check file is in `.github/workflows/`
- Verify YAML syntax (use online validator)
- Check branch name matches
- Verify trigger conditions

### Tests fail in CI but pass locally
- Check Python version
- Compare dependency versions
- Check environment differences
- Look at detailed CI logs

### Slow workflow execution
- Cache dependencies
- Reduce test matrix
- Skip linting/coverage on every PR
- Run expensive checks only on main

### Workflow quota exceeded
- GitHub Actions has free quota
- Optimize workflow to run faster
- Reduce scheduled runs
- Use workflow_dispatch for manual runs

---

**Last Updated:** August 18, 2026  
**GitHub Actions Version:** Latest  
**Workflows Included:** 3 (test, coverage, cross-browser)

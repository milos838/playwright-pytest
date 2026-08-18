# GitHub Actions Configuration

This directory contains GitHub Actions workflows for continuous integration and testing.

## Workflows

### test.yml - Main Test Suite
**Triggers:** Push to main/develop, Pull requests

**Jobs:**
- **test**: Runs full test suite on Python 3.10, 3.11, 3.12
- **smoke-tests**: Quick smoke test execution
- **code-quality**: Linting with flake8 and pylint
- **summary**: Summarizes test results

**Outputs:**
- HTML test reports (pytest-html)
- Test artifacts for failed tests
- Code quality checks

### coverage.yml - Code Coverage Analysis
**Triggers:** Push to main/develop, Pull requests, Daily at 2 AM UTC

**Jobs:**
- Generates test coverage report
- Uploads to Codecov
- Comments on PRs with coverage info

**Outputs:**
- Coverage XML report
- HTML coverage report
- Codecov integration

### cross-browser.yml - Cross-Browser Testing
**Triggers:** Scheduled (Monday & Friday 6 AM UTC), Manual dispatch

**Browsers Tested:**
- Chromium
- Firefox
- WebKit

**Outputs:**
- Cross-browser test reports
- Browser compatibility results

---

## Workflow Status

These workflows run automatically on:
- **Every push** to main or develop branches
- **Every pull request** to main or develop
- **Scheduled runs** as specified in each workflow
- **Manual triggers** (workflow_dispatch)

## Viewing Results

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Select workflow to view details
4. Click run to see detailed logs
5. Download artifacts for reports

## Modifying Workflows

To customize workflows:

1. Edit the YAML file in `.github/workflows/`
2. Commit and push changes
3. GitHub Actions will use the updated workflow
4. Test with a pull request first

## Common Customizations

### Change Python versions
```yaml
python-version: ['3.10', '3.11', '3.12']
```

### Change branches
```yaml
branches: [ main, develop, staging ]
```

### Add new schedule
```yaml
schedule:
  - cron: '0 2 * * *'  # Daily at 2 AM UTC
  - cron: '0 0 * * MON'  # Weekly on Monday
```

### Change test markers
```bash
pytest -m smoke  # Run only smoke tests
pytest -m "not slow"  # Skip slow tests
```

### Upload artifacts
```yaml
uses: actions/upload-artifact@v3
with:
  name: my-artifact
  path: path/to/files
  retention-days: 30
```

## Troubleshooting

### Workflow not running
- Check that workflow file is in `.github/workflows/`
- Verify YAML syntax is correct
- Check branch conditions match your branch
- Ensure events are correct

### Tests failing in CI but passing locally
- Check Python version matches
- Verify dependencies are installed
- Check environment variables
- Look at test logs in Actions

### Slow test execution
- Run smoke tests first
- Use parallel execution: `pytest -n auto`
- Reduce test matrix
- Cache dependencies

## Best Practices

1. **Keep workflows simple** - Use consistent patterns
2. **Fail fast** - Run quick checks first (smoke tests)
3. **Cache dependencies** - Speed up workflow runs
4. **Generate reports** - HTML reports help debugging
5. **Set retention** - Clean up old artifacts
6. **Monitor status** - Check workflow status regularly
7. **Use badges** - Add status badges to README
8. **Test matrix** - Test against multiple versions

## Status Badges

Add to your README.md:

```markdown
![Tests](https://github.com/milos838/playwright-pytest/workflows/Playwright%20Tests/badge.svg)
![Coverage](https://codecov.io/gh/milos838/playwright-pytest/branch/main/graph/badge.svg)
```

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)
- [Playwright in CI/CD](https://playwright.dev/python/docs/ci)

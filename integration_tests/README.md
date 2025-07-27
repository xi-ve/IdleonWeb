# Integration Tests

This directory contains Docker-based integration tests for IdleonWeb to ensure cross-platform compatibility and proper setup functionality.

## Overview

The integration tests verify:
- Setup script functionality on different platforms
- Dependency installation and management
- Plugin system loading and initialization
- Web UI system functionality
- Configuration file generation and validation
- File structure integrity

## Test Platforms

- **Arch Linux**: Tests pacman package manager and Arch-specific setup
- **Ubuntu**: Tests apt package manager and Debian-based setup
- **Windows**: Tests Windows-specific setup and Chocolatey package manager

## Running Tests

### Prerequisites

- Docker
- Docker Compose

### Quick Start (Recommended)

Use the automated test runner script:

```bash
# Run all platform tests
./run_integration_tests.sh

# Run specific platform tests
./run_integration_tests.sh arch
./run_integration_tests.sh ubuntu
./run_integration_tests.sh windows

# Clean up before running tests
./run_integration_tests.sh -c all

# Run with verbose output
./run_integration_tests.sh --verbose arch

# Show help
./run_integration_tests.sh --help
```

### Manual Docker Commands

If you prefer to run Docker commands directly:

```bash
# Test Arch Linux
docker compose --profile arch-test up --build

# Test Ubuntu
docker compose --profile ubuntu-test up --build

# Test Windows
docker compose --profile windows-test up --build

# Test all platforms
docker compose --profile all-test up --build
```

### Individual Platform Tests

```bash
# Arch Linux only
docker compose run --rm test-arch

# Ubuntu only
docker compose run --rm test-ubuntu

# Windows only
docker compose run --rm test-windows
```

### Local Testing

You can also run the tests locally without Docker:

```bash
# Test on current platform
python integration_tests/run_tests.py all

# Test specific platform simulation
python integration_tests/run_tests.py arch
python integration_tests/run_tests.py ubuntu
python integration_tests/run_tests.py windows
```

## Test Coverage

### Setup Tests
- Universal setup script (`setup.py`)
- Virtual environment creation
- Dependency installation (Python, Node.js, npm)

### System Tests
- Plugin system imports and initialization
- Web UI system functionality
- Configuration management
- File structure validation

### Integration Tests
- Main application script execution
- Module imports and dependencies
- Configuration file generation
- Cross-platform compatibility

## Test Results

Tests output detailed results including:
- Individual test pass/fail status
- Error messages and debugging information
- Summary of all test results
- Platform-specific issues

## Test Runner Script

The `run_integration_tests.sh` script provides a comprehensive way to run integration tests with:

### Features
- **Automated setup**: Checks Docker and Docker Compose availability
- **Platform selection**: Run tests for specific platforms or all platforms
- **Error reporting**: Detailed error information and troubleshooting tips
- **Resource management**: Automatic cleanup of Docker resources
- **Colored output**: Easy-to-read colored status messages
- **Flexible options**: Various command-line options for different use cases

### Script Options
- `-h, --help`: Show help message
- `-c, --clean`: Clean up Docker resources before running tests
- `-v, --verbose`: Show verbose output
- `--no-cleanup`: Don't clean up Docker resources after tests

### Error Handling
The script provides detailed error reporting including:
- Specific platform failure information
- Troubleshooting tips
- Commands to run for detailed debugging
- Resource cleanup recommendations

## Adding New Tests

To add new tests:

1. Add test function to `run_tests.py`
2. Include it in the `tests` list in `run_all_tests()`
3. Update Dockerfiles if new dependencies are needed

Example:
```python
def test_new_feature():
    print_status("Testing new feature...")
    # Test implementation
    return success

# Add to tests list
tests = [
    # ... existing tests
    ("New Feature", test_new_feature),
]
```

## Troubleshooting

### Common Issues

**Docker build fails:**
- Ensure Docker is running
- Check internet connection for package downloads
- Verify Dockerfile syntax

**Windows container fails on Linux:**
- Windows containers require Windows host
- Use GitHub Actions for cross-platform testing
- Run Windows tests directly on Windows machine

**Tests fail on specific platform:**
- Check platform-specific dependencies
- Verify package manager availability
- Review error logs for specific issues

**Permission issues:**
- Run Docker with appropriate permissions
- Check file ownership in mounted volumes

### Debug Mode

Run tests with verbose output:
```bash
docker-compose run --rm test-ubuntu bash
python integration_tests/run_tests.py ubuntu
```

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Test Arch Linux
  run: docker compose --profile arch-test up --build --exit-code-from test-arch

- name: Test Ubuntu
  run: docker compose --profile ubuntu-test up --build --exit-code-from test-ubuntu
```

## Platform-Specific Notes

### Arch Linux
- Uses `pacman` package manager
- Tests universal `setup.py` script functionality
- Verifies Arch-specific dependency paths

### Ubuntu
- Uses `apt` package manager
- Tests universal `setup.py` script
- Verifies Debian-based dependency management

### Windows
- Uses `Chocolatey` package manager
- Tests universal `setup.py` script functionality
- Verifies Windows path conventions and PowerShell execution
- **Note**: Windows containers require Windows host. Use GitHub Actions for cross-platform testing.

## Contributing

When adding new features:
1. Update integration tests to cover new functionality
2. Test on both platforms
3. Update Dockerfiles if new dependencies are required
4. Document any platform-specific considerations 
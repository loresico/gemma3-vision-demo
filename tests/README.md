# Tests

This directory contains the test suite for the Gemma3 Vision Demo application.

## Running Tests

### Install test dependencies

```bash
uv sync --extra dev
```

### Run all tests

```bash
pytest
```

### Run with coverage

```bash
pytest --cov=src --cov-report=html
```

Then open `htmlcov/index.html` in your browser to see the coverage report.

### Run specific test file

```bash
pytest tests/test_app.py
```

### Run specific test class or function

```bash
# Run a specific test class
pytest tests/test_app.py::TestGemma3VisionDemo

# Run a specific test function
pytest tests/test_app.py::TestGemma3VisionDemo::test_init_loads_model
```

### Run with verbose output

```bash
pytest -v
```

### Run tests matching a pattern

```bash
# Run only tests with "image" in the name
pytest -k "image"

# Run only tests that don't have "slow" in the name
pytest -k "not slow"
```

### Skip slow/integration tests

```bash
# Skip slow tests
pytest -m "not slow"

# Skip integration tests
pytest -m "not integration"

# Skip both
pytest -m "not slow and not integration"
```

### Run with print statements visible

```bash
pytest -s
```

## Test Structure

### `test_app.py`
Main test file containing:

- **TestGemma3VisionDemo**: Tests for the main application class
  - Initialization tests
  - Image analysis tests
  - Error handling tests
  - Interface creation tests

- **TestMonkeyPatch**: Tests for the mlx-vlm library patch
  - Verifies patch is applied correctly
  - Tests numpy to MLX array conversion

- **TestImageHandling**: Tests for image operations
  - Image creation and manipulation
  - File I/O operations

- **TestIntegration**: Integration tests (marked as slow)
  - Full pipeline tests with real model (skipped by default)
  - These require model download and are slow

- **TestParametrized**: Parametrized tests
  - Multiple input scenarios
  - Edge cases
  - Various image sizes

### `conftest.py`
Shared fixtures and configuration:
- Sample image fixtures (red, green, blue)
- Large image fixtures
- Custom pytest markers

## Test Coverage

Current test coverage focuses on:
- ✅ Model initialization
- ✅ Image analysis pipeline
- ✅ Error handling and edge cases
- ✅ Temporary file management
- ✅ Input validation
- ✅ Gradio interface creation
- ✅ Monkey patch functionality

## Writing New Tests

### Example test structure

```python
def test_my_feature(demo_app, sample_red_image):
    """Test description explaining what is being tested."""
    # Arrange
    expected_result = "some value"
    
    # Act
    result = demo_app.some_method(sample_red_image)
    
    # Assert
    assert result == expected_result
```

### Using fixtures

```python
def test_with_fixture(sample_red_image):
    """Fixtures are automatically provided by pytest."""
    assert sample_red_image.size == (100, 100)
```

### Using mocks

```python
from unittest.mock import Mock, patch

def test_with_mock():
    """Mock external dependencies."""
    with patch('module.function') as mock_func:
        mock_func.return_value = "mocked"
        # Test code here
        mock_func.assert_called_once()
```

### Parametrized tests

```python
@pytest.mark.parametrize("input,expected", [
    ("case1", "result1"),
    ("case2", "result2"),
])
def test_multiple_cases(input, expected):
    """Test multiple inputs efficiently."""
    assert process(input) == expected
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines. Most tests use mocks to avoid:
- Downloading large model files
- GPU/MLX requirements
- Network dependencies

Integration tests are marked and skipped by default in CI.

## Troubleshooting

### Import errors
```bash
# Make sure the package is installed in development mode
uv pip install -e .
```

### Module not found
```bash
# Ensure you're in the project root directory
cd /path/to/gemma3-vision-demo
pytest
```

### Coverage not working
```bash
# Install coverage plugin
uv pip install pytest-cov
```

## Best Practices

1. **Test one thing at a time** - Each test should verify a single behavior
2. **Use descriptive names** - Test names should explain what they test
3. **Arrange-Act-Assert** - Structure tests clearly
4. **Mock external dependencies** - Don't rely on external services
5. **Test edge cases** - Include None, empty strings, large inputs, etc.
6. **Keep tests fast** - Mark slow tests appropriately
7. **Write docstrings** - Explain what each test does

## Further Reading

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [Python Testing with pytest (Book)](https://pragprog.com/titles/bopytest/python-testing-with-pytest/)

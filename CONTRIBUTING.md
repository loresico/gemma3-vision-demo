# Contributing Guide

Thank you for considering contributing to Gemma 3 Vision Demo! This is a learning project exploring multimodal AI with Google DeepMind's Gemma 3 model on Apple Silicon. Your contributions help make this project a better learning resource for everyone.

## 📋 Table of Contents

- [Getting Started](#🚀-getting-started)
- [Commit Message Convention](#📝-Commit-Message-Convention)
- [Pull Request Process](#🔄-pull-request-process)
- [Development Setup](#🛠️-development-setup)
- [Testing](#testing)
- [Code Style](#🎨-code-style)
- [Theme Customization](#🎨-theme-customization)
- [Release Process](#📦-release-process)
- [Reporting Bugs](#🐛-reporting-bugs)
- [Feature Requests](#💡-feature-requests)
- [Areas for Contribution](#🌟-areas-for-contribution)

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/gemma3-vision-demo.git
cd gemma3-vision-demo

# Add upstream remote
git remote add upstream https://github.com/loresico/gemma3-vision-demo.git
```

### 2. Create a Branch

```bash
# Always create a new branch for your changes
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 3. Make Your Changes

Follow the project structure and coding standards (see below).

## 📝 Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

Must be one of:

- **feat**: New feature for the user
- **fix**: Bug fix for the user
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, whitespace)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to build process or auxiliary tools
- **ci**: Changes to CI configuration files and scripts
- **revert**: Reverts a previous commit

### Scope (Optional)

The scope should specify the place of the commit change:

- `app` - Main application code
- `theme` - UI/theme changes
- `model` - Model loading and inference
- `tests` - Test files
- `deps` - Dependency updates
- `docs` - Documentation
- `config` - Configuration files
- `ci` - CI/CD related

### Subject

- Use imperative, present tense: "add" not "added" nor "adds"
- Don't capitalize the first letter
- No period (.) at the end
- Maximum 50 characters

### Body (Optional)

- Use imperative, present tense
- Include motivation for the change
- Contrast with previous behavior

### Footer (Optional)

- Reference issues: `Closes #123`, `Fixes #456`
- Note breaking changes: `BREAKING CHANGE: description`

### Examples

#### Simple Feature
```
feat(theme): add ocean theme variant
```

#### Bug Fix with Details
```
fix(model): handle attention_mask type conversion

The mlx-vlm library expects mx.array but receives numpy array
for attention_mask. Added conversion in the patch.

Fixes #42
```

#### Documentation Update
```
docs(readme): update quick start instructions

Added information about gemma3-demo command and
installation in development mode.
```

#### Theme Change
```
feat(theme): add custom purple/pink color scheme

Changed from default blue theme to purple/pink for
better visual differentiation from other demos.
```

#### Dependency Update
```
chore(deps): upgrade gradio to 5.49.1

- Updated gradio from 5.0.0 to 5.49.1
- Includes new theme customization features
- No breaking changes
```

#### Test Addition
```
test(app): add integration tests for image processing

Added tests for image upload, processing pipeline,
and error handling with mock models.
```

## 🔄 Pull Request Process

### 1. Sync with Upstream

```bash
git fetch upstream
git rebase upstream/main
```

### 2. Run Tests and Checks

```bash
# Activate virtual environment
source .venv/bin/activate

# Format code
black src/ tests/

# Run tests with coverage
pytest tests/ --cov=src --cov-report=term-missing -v

# Run tests excluding slow/integration tests
pytest tests/ -m "not slow and not integration"

# Test the application manually
gemma3-demo
```

### 3. Push Your Changes

```bash
git push origin feature/your-feature-name
```

### 4. Create Pull Request

Go to GitHub and create a Pull Request with:

**Title:** Follow commit message convention
```
feat(setup): add Python 3.14 support
```

**Description Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Checklist
- [ ] My code follows the code style of this project
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] I have updated the documentation accordingly
- [ ] My commits follow the conventional commits specification

## Related Issues
Closes #(issue number)
```

### 5. Code Review

- Be open to feedback
- Respond to comments promptly
- Make requested changes in new commits
- Don't force-push after review has started

## 🛠️ Development Setup

### Prerequisites

- **Apple Silicon Mac** (M1/M2/M3) with 16GB+ RAM (required for MLX)
- Python 3.13+
- uv package manager
- Git

### Setup Development Environment

```bash
# Run setup script (downloads Python, installs uv and dependencies)
./setup.sh

# Activate virtual environment
source .venv/bin/activate

# Install package in development mode
uv pip install -e .

# Install dev dependencies
uv pip install -e ".[dev]"

# Verify installation
gemma3-demo
```

### Project Structure

```
gemma3-vision-demo/
├── .github/
│   └── workflows/
│       └── test.yml        # CI/CD test workflow
├── src/
│   └── gemma3_vision_demo/
│       ├── __init__.py
│       └── app.py          # Main application
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Pytest configuration
│   ├── test_app.py         # Application tests
│   └── README.md           # Test documentation
├── demo/                   # Screenshots/videos
├── setup.sh                # Setup script
├── verify_python_version.sh # Python version check
├── pyproject.toml          # Project configuration
├── pytest.ini              # Pytest settings
├── uv.lock                 # Locked dependencies
├── README.md               # Main documentation
├── CONTRIBUTING.md         # This file
├── TECHNICAL_NOTES.md      # Technical documentation
└── THEME_CUSTOMIZATION.md  # Theme guide
```

## 🧪 Testing

### Running Tests

```bash
# Activate environment
source .venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_app.py

# Run excluding slow/integration tests (CI default)
pytest tests/ -m "not slow and not integration"

# Run with verbose output
pytest -v

# Run and show print statements
pytest -s
```

### Writing Tests

- Use `pytest` framework
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive names
- Test edge cases
- Mock external dependencies (models, APIs)
- Add docstrings
- Use test markers for categorization

Example:
```python
import pytest
from unittest.mock import Mock, patch

def test_analyze_image_success(app_instance, sample_image):
    """Test image analysis with valid inputs."""
    with patch('src.gemma3_vision_demo.app.generate') as mock_generate:
        mock_generate.return_value = Mock(text="A beautiful landscape")
        
        result = app_instance.analyze_image(sample_image, "What do you see?")
        
        assert "beautiful landscape" in result.lower()
        mock_generate.assert_called_once()

@pytest.mark.slow
def test_real_model_inference():
    """Integration test with real model (slow)."""
    # This test will be skipped in CI
    pass
```

### Test Markers

Available markers in `pytest.ini`:
- `slow` - Tests that take a long time (>5 seconds)
- `integration` - Integration tests requiring real models
- `unit` - Fast unit tests (default)

See `tests/README.md` for comprehensive testing guide.

## 🎨 Code Style

### Python

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for formatting (88 char line length)
- Use type hints where appropriate
- Write docstrings for functions and classes (Google style)
- Keep functions focused and single-purpose
- Add type annotations from `__future__ import annotations`

```python
from __future__ import annotations

import gradio as gr
from PIL import Image


def analyze_image(image: Image.Image, question: str) -> str:
    """
    Analyze an image and answer a question about it.
    
    Args:
        image: PIL Image to analyze
        question: Question to answer about the image
        
    Returns:
        Answer text from the model
        
    Raises:
        ValueError: If image is None or question is empty
    """
    if image is None:
        raise ValueError("Image cannot be None")
    if not question.strip():
        raise ValueError("Question cannot be empty")
    
    # Process image and generate answer
    return model.generate(image, question)
```

### Gradio UI Code

- Use descriptive component labels
- Add helpful placeholder text
- Organize layout with `gr.Row()` and `gr.Column()`
- Include example inputs with `gr.Examples()`
- Use markdown for formatting instructions

```python
with gr.Blocks(theme=custom_theme) as demo:
    gr.Markdown("# My Demo Title")
    
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(type="pil", label="Upload Image")
            submit_btn = gr.Button("Submit", variant="primary")
        
        with gr.Column():
            output = gr.Markdown(label="Result")
```

### Bash Scripts

- Use `set -e` for error handling
- Add comments for complex logic
- Use meaningful variable names
- Quote variables: `"$var"` not `$var`

```bash
#!/usr/bin/env bash
set -e

# Configuration
PYTHON_VERSION="3.13"

echo "Setting up Python ${PYTHON_VERSION}..."
```

### Documentation

- Use Markdown for documentation
- Include code examples with proper syntax highlighting
- Keep it concise and clear
- Update README.md when adding user-facing features
- Update TECHNICAL_NOTES.md for implementation details
- Update THEME_CUSTOMIZATION.md for UI changes
- Add inline comments for complex logic (especially MLX operations)
- Document workarounds and patches thoroughly

Example inline documentation:
```python
# WORKAROUND: mlx-vlm v0.3.5 expects mx.array but receives numpy array
# Convert attention_mask to MLX array before processing
if isinstance(attention_mask, np.ndarray):
    attention_mask = mx.array(attention_mask)
```

## 🎨 Theme Customization

### Changing the UI Theme

The app uses a custom Gradio theme builder function. To customize:

1. **Edit theme parameters** in `src/gemma3_vision_demo/app.py`:

```python
custom_theme = build_custom_theme(
    base_theme="soft",        # Options: "soft", "default", "glass", "monochrome", "ocean"
    primary_color="purple",   # Try: "blue", "green", "purple", "orange", "pink"
    secondary_color="pink",   # Any valid color name
    neutral_color="slate"     # Options: "slate", "gray", "zinc", "neutral", "stone"
)
```

2. **Test your changes**:

```bash
source .venv/bin/activate
gemma3-demo
```

3. **Popular theme combinations**:

```python
# Professional Blue (default)
build_custom_theme(primary_color="blue", secondary_color="cyan")

# Vibrant Purple
build_custom_theme(primary_color="purple", secondary_color="pink")

# Modern Green Glass
build_custom_theme(base_theme="glass", primary_color="green")

# Ocean Theme
build_custom_theme(base_theme="ocean", primary_color="blue", secondary_color="teal")
```

4. **Document your theme**:
   - Update `THEME_CUSTOMIZATION.md` if you add new theme presets
   - Include screenshots in PRs that modify the theme

See `THEME_CUSTOMIZATION.md` for comprehensive theme guide.

## 📦 Release Process

(For Maintainers)

### Version Bump

```bash
# Update version in pyproject.toml
# Update CHANGELOG.md
# Commit with conventional commit
git commit -m "chore(release): bump version to 1.0.0"
```

### Tagging

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## 🐛 Reporting Bugs

### Before Reporting

- Check existing issues
- Try latest version
- Verify it's reproducible

### Bug Report Template

```markdown
**Describe the bug**
A clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Run '...'
2. See error

**Expected behavior**
What you expected to happen

**Environment**
- OS: [e.g., macOS 14.0 Sonoma]
- Mac Model: [e.g., MacBook Pro M2, 16GB RAM]
- Python version: [e.g., 3.13]
- Gradio version: [e.g., 5.49.1]
- MLX-VLM version: [e.g., 0.3.5]
- Error output: [paste here]

**Additional context**
Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem

**Describe the solution you'd like**
A clear description of what you want to happen

**Describe alternatives you've considered**
Other solutions you've thought about

**Additional context**
Any other context or screenshots
```

## 🌟 Areas for Contribution

We especially welcome contributions in these areas:

### Features
- **Streaming responses** - Implement real-time token streaming
- **Batch processing** - Process multiple images at once
- **History/session management** - Save conversation history
- **Advanced prompting** - Pre-built prompt templates
- **Export functionality** - Save results to file

### Model Improvements
- **Fine-tuning examples** - Domain-specific fine-tuning guides
- **Model comparison** - Support for different Gemma variants (12B, 27B)
- **Performance optimization** - Faster inference, lower memory usage

### UI/UX
- **Theme presets** - Additional color schemes
- **Dark mode** - Proper dark theme support
- **Responsive design** - Better mobile/tablet support
- **Accessibility** - Screen reader support, keyboard navigation

### Documentation
- **Tutorials** - Step-by-step guides for common tasks
- **Examples** - More example images and questions
- **Architecture diagrams** - Visual documentation of the system
- **Video demos** - Screen recordings of features

### Testing
- **Integration tests** - End-to-end testing with real models
- **Performance benchmarks** - Track inference speed and memory usage
- **UI tests** - Automated Gradio interface testing

## 🙏 Thank You!

This is a learning project, and your contributions help make it a valuable resource for the ML/AI community. Whether you're fixing a typo, adding a feature, or just asking questions, you're helping improve this project for everyone!

---

**Happy Contributing! 🎉**

*Remember: This is a learning project - don't hesitate to ask questions or propose new ideas!*
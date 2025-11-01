# Gemma 3 Vision Q&A Demo

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![UV](https://img.shields.io/badge/uv-enabled-blue)](https://github.com/astral-sh/uv)
[![Portable](https://img.shields.io/badge/portable-100%25-green)](https://github.com/indygreg/python-build-standalone)

**Learning Project**: Hands-on exploration of Google DeepMind's Gemma 3 multimodal model

Built with modern Python tooling (uv) to demonstrate:
- Large language model (LLM) deployment
- Multimodal AI (vision + language)
- MLX optimization for Apple Silicon
- Modern Python package management

## Quick Start
```bash
# Clone repository
git clone https://github.com/loresico/gemma3-vision-demo
cd gemma3-vision-demo

# Download python, install uv and then dependencies as in uv.lock
./setup.sh

# Activate the .venv
source .venv/bin/activate

# Run application
# Using installed command (recommended)
gemma3-demo

# Using module directly
python -m src.gemma3_vision_demo.app
```

## Demo

[Screenshots or video here]

## Technical Stack

- **Model**: Gemma 3 4B (8-bit quantized)
- **Framework**: MLX (Apple Silicon optimized)
- **Package Manager**: uv (fast Python package installer)
- **Interface**: Gradio
- **Python**: 3.10+

## Project Structure
```
gemma3-vision-demo/
├── .github/
│   └── workflows/
│       ├── ci.yml          # CI/CD pipeline
│       └── test.yml        # Test workflow
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
├── htmlcov/                # Coverage reports (generated)
├── pyproject.toml          # Project configuration
├── uv.lock                 # Locked dependencies
├── pytest.ini              # Pytest settings
├── setup.sh                # Setup script
├── verify_python_version.sh # Python version check
├── README.md               # This file
├── CONTRIBUTING.md         # Contribution guidelines
├── TECHNICAL_NOTES.md      # Technical documentation
└── QUICK_REFERENCE.md      # Quick reference guide
```

## Known Issues

### mlx-vlm v0.3.5 Compatibility
This project includes a workaround for a bug in mlx-vlm v0.3.5 where the Gemma3 model's attention_mask handling causes a TypeError. The fix is applied automatically via a runtime patch in `app.py`. This workaround can be removed once the upstream library is updated.

## Limitations

This is a learning/demo project with:
- Local-only execution (no cloud deployment)
- Requires Apple Silicon Mac with 16GB+ RAM
- Model quantized to 8-bit for efficiency
- Not optimized for production use

## Future Exploration

- Fine-tune on domain-specific imagery (maps, satellite data)
- Implement streaming responses
- Add batch processing capabilities
- Explore larger Gemma variants (12B, 27B)
- Integration with mapping APIs

## Acknowledgments

- Google DeepMind for open-sourcing Gemma 3
- MLX team for Apple Silicon optimization
- Astral (uv developers) for modern Python tooling

## License

MIT - Demo/learning project

---

**Part of my active learning in ML/AI:**
- [Computer Vision: Image Super-Resolution](https://huggingface.co/spaces/loresico/gradio-super-resolution)
- [ML: Coffee Compass Predictor](https://huggingface.co/spaces/loresico/coffee-compass)
- [Python Templates with uv/Poetry](https://github.com/loresico/template-python-uv)
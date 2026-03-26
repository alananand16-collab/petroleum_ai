# Contributing to Petroleum AI Assistant

Thank you for your interest in contributing to the Petroleum AI Assistant! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/petroleum_ai.git
   cd petroleum_ai
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\Activate.ps1
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes using Google-style format
- Add type hints to function parameters and return values

### Commits

- Write clear, descriptive commit messages
- Use the present tense: "Add feature" not "Added feature"
- Reference issues when relevant: "Fix #123"
- Keep commits focused and atomic

### Pull Request Process

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with clear messages

3. Push to your fork and create a Pull Request:
   - Provide a clear description of the changes
   - Reference any related issues
   - Include screenshots or examples if applicable

4. Ensure all checks pass before requesting review

## Types of Contributions

### Bug Reports

When reporting a bug, please include:
- Description of the issue
- Steps to reproduce
- Expected and actual behavior
- Python version and OS
- Error messages or logs

### Feature Requests

For new features:
- Provide clear use case and motivation
- Explain how it benefits petroleum engineering professionals
- Suggest implementation approach if possible

### Documentation

- Fix typos and clarify existing documentation
- Add examples for hard-to-understand features
- Improve README sections
- Add inline code comments where logic is complex

### Code Improvements

- Refactor code for better readability or performance
- Add missing type hints
- Improve error handling
- Optimize performance

## Testing Guidelines

- Test new features thoroughly before submitting PR
- Ensure existing functionality still works
- Test edge cases and error conditions
- Provide test examples in PR description

## Documentation Standards

### Module Docstrings

```python
"""Brief module description.

Detailed description of what this module does, including:
- Key functions and their purposes
- Important classes and their roles
"""
```

### Function Docstrings

```python
def function_name(param1: str, param2: int) -> dict:
    """Brief one-line description.

    Longer description explaining what the function does,
    including any important details about behavior.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When specific condition is met.
    """
```

## Project Structure

```
petroleum_ai/
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── chatbot.py         # Gradio web interface
│   ├── ingest.py          # Document processing pipeline
│   └── utils.py           # Utility functions
├── docs/                  # PDF documents for ingestion
├── vectorstore/           # Chroma vector database
├── requirements.txt       # Python dependencies
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## Running the Application

### Ingesting Documents

```bash
python src/ingest.py
```

### Starting the Chatbot

```bash
python src/chatbot.py
```

## Configuration

Edit the `.env` file to configure:
- `GOOGLE_API_KEY`: Your Google Generative AI API key
- `GOOGLE_MODEL`: LLM model to use (default: gemini-2.5-flash)
- `LLM_TEMPERATURE`: Response creativity (0-1)
- `TOP_K_RESULTS`: Number of context documents to retrieve
- `OCR_DPI`: DPI for OCR processing
- `CHUNK_SIZE`: Document chunk size for vectorization

## Code Review

Your PR will be reviewed for:
- Code quality and style consistency
- Type hints and docstrings
- Error handling
- Performance considerations
- Documentation updates

## Questions or Need Help?

- Open a GitHub issue for questions
- Check existing issues for similar discussions
- Review the README for common setups

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to make petroleum engineering AI more accessible! 🛢️🤖

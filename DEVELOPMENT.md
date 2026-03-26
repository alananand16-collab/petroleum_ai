# Development Guide

This guide provides detailed information for developers working on the Petroleum AI Assistant project.

## Project Structure

```
petroleum_ai/
├── src/
│   ├── __init__.py              # Package metadata
│   ├── config.py                # Configuration management
│   ├── chatbot.py               # Main chatbot interface
│   ├── ingest.py                # Document ingestion pipeline
│   └── utils.py                 # Shared utility functions
├── docs/                        # PDF documents (not in repo)
├── vectorstore/                 # Vector database (generated, not in repo)
├── .github/workflows/           # GitHub Actions CI/CD
├── .env.example                 # Example environment variables
├── requirements.txt             # Python dependencies
└── README.md                    # Main documentation
```

## Core Modules

### config.py

Manages all configuration using environment variables.

```python
from src.config import Config

# Access configuration
api_key = Config.GOOGLE_API_KEY
model = Config.GOOGLE_MODEL
```

Environment variables override defaults. See `.env.example` for all options.

### utils.py

Provides shared utilities:

- `setup_logging()` - Configures application logging
- `format_documents()` - Formats LangChain documents for context
- `extract_sources()` - Extracts source metadata from documents
- `format_sources()` - Formats sources for display

### ingest.py

Handles document processing:

1. **load_documents_with_text()** - PyMuPDF text extraction
2. **load_documents_with_ocr()** - RapidOCR for scanned PDFs
3. **load_and_process_documents()** - Main loading orchestration
4. **split_documents()** - Document chunking
5. **create_and_store_vectordb()** - Vector database creation

Run with: `python src/ingest.py`

### chatbot.py

Provides the main interface:

1. **PetroleumAIAssistant** - Core RAG implementation
2. **create_interface()** - Gradio UI builder
3. **main()** - Application entry point

Run with: `python src/chatbot.py`

## Development Workflow

### Setting Up

```bash
# Clone and navigate
git clone <repository>
cd petroleum_ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API key and settings
```

### Running Tests

```bash
# Syntax check
python -m py_compile src/*.py

# Import verification
python -c "from src import config, utils, ingest, chatbot"

# Run linting
flake8 src/
black src/
isort src/
```

### Common Development Tasks

#### Adding New Configuration Options

1. Add to `config.py` in the `Config` class:
   ```python
   NEW_OPTION: str = os.getenv("NEW_OPTION", "default_value")
   ```

2. Add to `.env.example`:
   ```env
   NEW_OPTION=default_value
   ```

3. Update documentation in `README.md` configuration table

#### Adding New Utility Functions

Add to `utils.py` with:
- Clear docstring (Google style)
- Type hints
- Error handling

```python
def new_utility(param: str) -> dict:
    """Brief description.
    
    Longer description here.
    
    Args:
        param: Parameter description.
        
    Returns:
        Return value description.
    """
    # Implementation
    return result
```

#### Improving Error Handling

Use logging for errors:

```python
try:
    # Operation
    result = do_something()
except SomeError as e:
    logger.error(f"Operation failed: {e}")
    raise
except OtherError as e:
    logger.warning(f"Operation partially failed: {e}")
    return default_value
```

## Working with Documents

### Supported Formats

- **Native PDFs**: Direct text extraction with PyMuPDF ✓
- **Scanned PDFs**: OCR processing with RapidOCR ✓
- **Mixed PDFs**: Automatic fallback to OCR when needed ✓

### Optimizing PDF Processing

```bash
# Faster processing (lower OCR quality)
export OCR_DPI=75
python src/ingest.py

# Higher quality (slower processing)
export OCR_DPI=300
python src/ingest.py

# Limit pages for testing
export OCR_MAX_PAGES=5
python src/ingest.py
```

## Debugging

### Enable Debug Logging

```python
from src.utils import setup_logging
logger = setup_logging(level="DEBUG")
```

Or via environment:
```bash
LOGLEVEL=DEBUG python src/chatbot.py
```

### Testing Vector Database

```python
from src.config import Config
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Load database
embedding = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)
vectordb = Chroma(
    embedding_function=embedding,
    persist_directory=Config.VECTORSTORE_PATH
)

# Query
results = vectordb.similarity_search("your query", k=3)
for doc in results:
    print(f"Source: {doc.metadata['source']}")
    print(f"Content: {doc.page_content[:100]}...")
```

### Common Issues

**Error: "GOOGLE_API_KEY is not set"**
- Ensure `.env` file exists with `GOOGLE_API_KEY=...`
- Check environment variable is set: `echo $GOOGLE_API_KEY`

**Error: "No PDF files found"**
- Add PDFs to `docs/` folder
- Verify folder path in config
- Check PDF file permissions

**Error: "Vector database not found"**
- Run `python src/ingest.py` first to create database
- Verify `vectorstore/` directory exists
- Check configuration `VECTORSTORE_PATH`

**Slow OCR Processing**
- Reduce `OCR_DPI` in .env (default 150)
- Limit `OCR_MAX_PAGES` for initial testing
- Or pre-process scanned PDFs with better tools

## Performance Optimization

### Document Chunking

Fine-tune in `.env`:
```env
CHUNK_SIZE=500      # Larger = fewer chunks, faster but less precise
CHUNK_OVERLAP=50    # More overlap = better context retention
```

### Search Configuration

Adjust in `.env`:
```env
TOP_K_RESULTS=3     # More results = slower but more context
```

### LLM Configuration

```env
LLM_TEMPERATURE=0.3  # Lower = more deterministic
```

## Type Hints and Documentation

All new code should include:

1. **Type hints** for parameters and returns:
   ```python
   def process(items: List[str], count: int) -> Dict[str, int]:
   ```

2. **Google-style docstrings**:
   ```python
   """Brief description.
   
   Longer description.
   
   Args:
       param1: Description.
       
   Returns:
       Description.
       
   Raises:
       ValueError: When condition.
   """
   ```

3. **Error handling with logging**:
   ```python
   try:
       result = operation()
   except Exception as e:
       logger.error(f"Failed: {e}")
       raise
   ```

## Contributing Code

1. **Create feature branch**: `git checkout -b feature/name`
2. **Write code** with type hints and docstrings
3. **Run quality checks**: `black`, `isort`, `flake8`
4. **Test locally**: Verify ingestion and chatbot work
5. **Commit clearly**: `git commit -m "Add feature: clear description"`
6. **Push and create PR**: Include description of changes

## Code Style

Uses Black for formatting:

```bash
# Format code
black src/

# Check formatting
black --check src/

# Sort imports
isort src/
```

## Publishing and Releases

See the repository's GitHub Actions workflows:
- `code-quality.yml` - Continuous quality checks
- `test.yml` - Automated testing
- `documentation.yml` - Documentation validation

## Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [LangChain Documentation](https://python.langchain.com/)
- [Chroma Vector DB](https://docs.trychroma.com/)

---

For questions, open an issue or check [CONTRIBUTING.md](CONTRIBUTING.md).

# Petroleum Engineering AI Assistant 🛢️🤖

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)

A sophisticated AI-powered assistant designed specifically for upstream petroleum engineering. This application utilizes Retrieval-Augmented Generation (RAG) to provide accurate, context-aware answers to complex domain questions.

## 🌟 Features

- **Specialized Knowledge Base**: Powered by advanced vector representations of petroleum engineering literature
- **State-of-the-Art LLM Integration**: Uses Google's generative AI models for high-quality responses
- **Smart Document Processing**: Dual-mode extraction with OCR fallback for scanned documents
- **Interactive Web Interface**: Easy-to-use Gradio web interface for seamless interaction
- **Source Attribution**: Transparently cites sources for answers to ensure technical accuracy and trustworthiness
- **Production-Ready**: Comprehensive error handling, logging, and configuration management
- **Type-Safe**: Full type hints throughout codebase for maintainability

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | LangChain, Gradio |
| **Embeddings** | HuggingFace (`all-MiniLM-L6-v2`) |
| **Vector Database** | Chroma |
| **LLM** | Google Gemini (`gemini-2.5-flash`) |
| **OCR Engine** | RapidOCR for scanned documents |
| **Language** | Python 3.8+ |

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 📦 Prerequisites

- Python 3.8 or higher
- Google API Key ([Get one here](https://ai.google.dev))
- 2GB+ of free disk space (for vector database)

## 🚀 Installation

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alananand16-collab/petroleum_ai.git
   cd petroleum_ai
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** by creating a `.env` file:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   GOOGLE_MODEL=gemini-2.5-flash
   LLM_TEMPERATURE=0.3
   TOP_K_RESULTS=3
   CHUNK_SIZE=500
   CHUNK_OVERLAP=50
   OCR_DPI=150
   GRADIO_PORT=7860
   ```

5. **Add your PDF documents** to the `docs/` folder

## ⚙️ Configuration

The application uses environment variables for configuration. Create a `.env` file with the following options:

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_API_KEY` | - | **Required**. Your Google Generative AI API key |
| `GOOGLE_MODEL` | `gemini-2.5-flash` | LLM model to use |
| `VECTORSTORE_PATH` | `vectorstore` | Path to store the vector database |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | HuggingFace embedding model |
| `LLM_TEMPERATURE` | `0.3` | Response creativity (0.0-1.0) |
| `TOP_K_RESULTS` | `3` | Number of context documents to retrieve |
| `CHUNK_SIZE` | `500` | Document chunk size for vectorization |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `OCR_DPI` | `150` | DPI for OCR image processing |
| `OCR_MAX_PAGES` | - | Max pages per PDF for OCR (empty = all) |
| `GRADIO_PORT` | `7860` | Port for Gradio interface |
| `GRADIO_SHARE` | `false` | Share public Gradio link |

## 📖 Usage

### 1. Prepare Your Documents

Place petroleum engineering PDFs in the `docs/` folder. The system supports:
- Text-extractable PDFs (standard PDFs)
- Scanned PDFs (automatically processed with OCR)

### 2. Ingest Documents

Run the ingestion pipeline to process PDFs and create the vector database:

```bash
python src/ingest.py
```

Expected output:
```
==================================================
Starting Document Ingestion Pipeline
==================================================
Found 3 PDF files to process
Loading document_1.pdf...
  ✓ document_1.pdf: extracted 45 pages
...
Total: loaded 150 pages from 3 files
Splitting documents into chunks...
Created 450 chunks
Kept 448 non-empty chunks
Creating vector database...
✓ Vector database created and saved to vectorstore
==================================================
✓ Document ingestion completed successfully!
==================================================
```

### 3. Start the Chatbot

Launch the interactive web interface:

```bash
python src/chatbot.py
```

The interface will be available at: `http://localhost:7860`

### Example Queries

- "What is enhanced oil recovery and its methods?"
- "Explain waterflooding and its effectiveness"
- "What are the main challenges in deep-water drilling?"
- "How does pressure maintenance affect oil production?"
- "Describe the life cycle of an oil field"

## 🏗️ Architecture

```
petroleum_ai/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration management
│   ├── chatbot.py               # Gradio web interface
│   ├── ingest.py                # Document processing pipeline
│   └── utils.py                 # Utility functions and logging
├── docs/                        # Input PDF documents
├── vectorstore/                 # Chroma vector database (generated)
├── .github/
│   └── workflows/               # GitHub Actions CI/CD
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (gitignored)
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
├── LICENSE                      # MIT License
└── CONTRIBUTING.md              # Contributing guidelines
```

### Pipeline Flow

```
PDF Documents (docs/)
        ↓
   [Text Extraction]
        ↓
   [OCR Fallback] ← for scanned PDFs
        ↓
   [Text Splitting]
        ↓
   [Vectorization]
        ↓
[Chroma Vector DB]
        ↓
    [RAG Chain]
        ↓
  [LLM Response]
        ↓
 [Web Interface]
```

## 🔒 Security

- **Never commit `.env` files** or any files containing API keys
- The `.gitignore` is pre-configured to protect sensitive files
- API keys are loaded only from environment variables
- Vector database is stored locally and never uploaded

## 🧪 Development

### Setting Up Development Environment

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run code quality checks
black src/
isort src/
flake8 src/
```

### Code Standards

- **Type Hints**: All functions must have type hints
- **Docstrings**: All functions/classes must have docstrings (Google style)
- **Logging**: Use logging module instead of print statements
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Testing**: Test edge cases and error conditions

### Testing Locally

```bash
# Test document ingestion
python src/ingest.py

# Test chatbot interface
python src/chatbot.py
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- Submitting bug reports
- Suggesting features
- Writing code
- Creating pull requests

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Chroma Documentation](https://docs.trychroma.com/)
- [Gradio Documentation](https://gradio.app/)
- [Google AI Studio](https://ai.google.dev/)
- [Petroleum Engineering Knowledge](https://onepetro.org/)

## 👤 Author

**Alan**

## 💬 Questions or Support?

- 📖 Check the [CONTRIBUTING.md](CONTRIBUTING.md) for development questions
- 🐛 Open an [Issue](https://github.com/alananand16-collab/petroleum_ai/issues) for bug reports
- 💡 Start a [Discussion](https://github.com/alananand16-collab/petroleum_ai/discussions) for ideas

---

<p align="center">
  Made with ❤️ for petroleum engineers worldwide
</p>

<p align="center">
  ⭐ If this project helps you, please consider giving it a star!
</p>

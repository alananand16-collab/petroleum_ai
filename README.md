# Petroleum Engineering AI Assistant 🛢️🤖

A sophisticated AI-powered assistant designed specifically for upstream petroleum engineering. This application utilizes Retrieval-Augmented Generation (RAG) to provide accurate, context-aware answers to complex domain questions.

## Features ✨
- **Specialized Knowledge Base**: Powered by advanced vector representations of petroleum engineering literature.
- **State-of-the-Art LLM Integration**: Uses Google's generative AI models for high-quality responses.
- **Interactive Interface**: Easy-to-use Gradio web interface.
- **Source Attribution**: Transparently cites sources for its answers to ensure technical accuracy and trustworthiness.

## Tech Stack 🛠️
- **Framework**: LangChain, Gradio
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Vector Database**: Chroma
- **LLM**: Google Gemini (`gemini-2.5-flash`)

## Getting Started 🚀

### Prerequisites
- Python 3.8+
- A Google API Key (`GOOGLE_API_KEY`)

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables by creating a `.env` file:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   GOOGLE_MODEL=gemini-2.5-flash
   ```

### Usage
Run the chatbot:
```bash
python src/chatbot.py
```
This will launch a Gradio interface in your web browser.

## Security Note 🔒
This repository is configured to securely ignore sensitive files such as `.env` and virtual environments. Ensure you never commit API keys to version control.

# Troubleshooting Guide

Common issues and solutions for the Petroleum AI Assistant.

## Installation Issues

### Issue: Python version too old

```
Error: Python 3.8+ is required
```

**Solution:**
- Check Python version: `python --version`
- Install Python 3.8+: [python.org](https://www.python.org/downloads/)
- Use `python3` on macOS/Linux if `python` points to Python 2

### Issue: pip command not found

```
Error: 'pip' is not recognized as an internal or external command
```

**Solution:**
```bash
# Windows
python -m pip install -r requirements.txt

# macOS/Linux
python3 -m pip install -r requirements.txt
```

### Issue: Virtual environment activation fails

```
Error: venv\Scripts\Activate.ps1 cannot be loaded
```

**Solution (Windows PowerShell):**
```powershell
# Allow script execution (one-time)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
venv\Scripts\Activate.ps1
```

## Configuration Issues

### Issue: GOOGLE_API_KEY not found

```
Configuration error: GOOGLE_API_KEY environment variable is not set
```

**Solution:**
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create `.env` file in project root:
   ```env
   GOOGLE_API_KEY=your_actual_key_here
   ```
3. Restart the application
4. Verify: `python -c "from src.config import Config; Config.validate()"`

### Issue: Another application is using port 7860

```
Error: Port 7860 is already in use
```

**Solution:**

Option 1 - Use different port:
```bash
export GRADIO_PORT=7861
python src/chatbot.py
```

Option 2 - Kill existing process (Linux/macOS):
```bash
lsof -ti:7860 | xargs kill -9
```

Option 3 - Kill process (Windows):
```powershell
Get-Process | Where-Object {$_.Ports -eq 7860} | Stop-Process
# Or find and use Task Manager
```

## Document Processing Issues

### Issue: No PDFs found in docs folder

```
ValueError: No PDF files found in docs/
```

**Solution:**
1. Create `docs/` folder: `mkdir docs`
2. Add PDF files to the folder
3. Verify with: `ls docs/` (or `dir docs` on Windows)
4. Check file permissions (files should be readable)

### Issue: PDF extraction fails

```
Failed to extract text from document.pdf
```

**Causes & Solutions:**

**Text-extractable PDF not working:**
- Verify PDF is not corrupted: Try opening in PDF reader
- Try OCR fallback (will happen automatically)
- Increase `OCR_DPI` for better quality:
  ```bash
  export OCR_DPI=200
  python src/ingest.py
  ```

**OCR keeps failing:**
- Check OCR dependencies: `pip install rapidocr-onnxruntime`
- Try lower DPI (faster): `export OCR_DPI=100`
- Limit pages for testing: `export OCR_MAX_PAGES=3`

### Issue: Out of memory during ingestion

```
MemoryError: Unable to allocate memory
```

**Solutions:**
1. **Reduce OCR DPI** (uses more memory with higher values):
   ```bash
   export OCR_DPI=100
   ```

2. **Limit pages per PDF**:
   ```bash
   export OCR_MAX_PAGES=50
   ```

3. **Reduce chunk size**:
   ```bash
   export CHUNK_SIZE=300
   ```

4. **Process one PDF at a time** - Remove others from `docs/` folder

5. **Increase system swap** (advanced):
   - Linux: Create swap file
   - Windows: Extend virtual memory
   - macOS: Use Activity Monitor

### Issue: Vector database corrupted

```
Error: Could not load Chroma database
```

**Solution:**
```bash
# Backup old database
mv vectorstore vectorstore.backup

# Recreate by re-running ingestion
python src/ingest.py
```

## Runtime Issues

### Issue: Empty response from chatbot

```
"❌ I couldn't find relevant information in the knowledge base"
```

**Solutions:**
1. **Verify documents were ingested**: Check for messages in `python src/ingest.py`
2. **Check query relevance**: Try different keywords
3. **Increase search results**:
   ```env
   TOP_K_RESULTS=5
   ```
4. **Check document quality**: PDFs should contain readable text

### Issue: Slow responses from chatbot

**Causes & Solutions:**

**1. Network/API latency:**
- Check internet connection
- Google API might be slow - try again later
- Use `LLM_TEMPERATURE=0.1` for faster responses

**2. Large vector database:**
```bash
# Reduce context size
export TOP_K_RESULTS=1

# Or limit pages during ingestion
export OCR_MAX_PAGES=100
```

**3. System performance:**
- Close other applications
- Check available RAM: 4GB minimum recommended
- Check CPU usage

### Issue: Incorrect or hallucinated answers

**Solutions:**
1. **Lower temperature** for more factual responses:
   ```env
   LLM_TEMPERATURE=0.1
   ```

2. **Improve document quality**:
   - Ensure PDFs contain accurate information
   - Remove incorrect or outdated documents
   - Re-run ingestion: `python src/ingest.py`

3. **Increase context**:
   ```env
   TOP_K_RESULTS=5
   ```

## Logging and Debugging

### Enable debug logging

```bash
python -c "
import os
os.environ['LOGLEVEL'] = 'DEBUG'
from src.chatbot import main
main()
"
```

### Check what's in vector database

```python
from src.config import Config
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)
vectordb = Chroma(
    embedding_function=embedding,
    persist_directory=Config.VECTORSTORE_PATH
)

# Check database contents
print(f"Total items in database: {vectordb._collection.count()}")

# Test a query
results = vectordb.similarity_search("oil production", k=3)
for i, doc in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print(f"Source: {doc.metadata.get('source', 'unknown')}")
    print(f"Page: {doc.metadata.get('page', 'unknown')}")
    print(f"Content: {doc.page_content[:200]}...")
```

## Performance Optimization

### For faster startup:

```bash
# Reduce embedding model size (trade-off: lower quality)
export EMBEDDING_MODEL=all-MiniLM-L6-v2

# Pre-load in background
python src/ingest.py &
sleep 60  # Let it load
python src/chatbot.py
```

### For faster ingestion:

```bash
# Skip OCR for known good PDFs
export OCR_DPI=150

# Larger chunks (fewer, faster processing)
export CHUNK_SIZE=1000
export CHUNK_OVERLAP=100
```

### For faster queries:

```bash
# Fewer search results
export TOP_K_RESULTS=1

# Higher temperature (deterministic)
export LLM_TEMPERATURE=0.1
```

## Getting Help

1. **Check logs**: Look for detailed error messages in terminal
2. **Review documentation**: See [README.md](README.md) and [DEVELOPMENT.md](DEVELOPMENT.md)
3. **Open an issue**: [GitHub Issues](https://github.com/alananand16-collab/petroleum_ai/issues)
4. **Check FAQ** below

## FAQ

**Q: Can I use a different LLM?**
A: Yes, see `config.py` and use any LangChain LLM supported model.

**Q: Can I add custom documents after initial setup?**
A: Yes, add PDFs to `docs/` and re-run `python src/ingest.py` to update the database.

**Q: How do I update dependencies?**
A: Run `pip install -r requirements.txt --upgrade`

**Q: Will my data be shared?**
A: No, everything runs locally except API calls to Google's LLM.

**Q: How can I improve response quality?**
A: Use higher quality PDFs, tune `TOP_K_RESULTS`, and lower `LLM_TEMPERATURE`.

**Q: Can I run this without internet?**
A: No, the LLM requires API calls. Embeddings can run locally but API is required.

---

Not found your issue? [Open a GitHub issue](https://github.com/alananand16-collab/petroleum_ai/issues) with:
- Detailed error message
- Steps to reproduce
- Python version
- OS and environment info

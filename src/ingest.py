from pathlib import Path
import os

import fitz
import numpy as np
from langchain_core.documents import Document
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from rapidocr_onnxruntime import RapidOCR


def load_documents_with_text(pdf_path):
    return PyMuPDFLoader(str(pdf_path)).load()


def load_documents_with_ocr(pdf_path, ocr_engine, ocr_dpi=150, max_pages=None):
    ocr_docs = []
    with fitz.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf, start=1):
            if max_pages is not None and page_idx > max_pages:
                break

            pix = page.get_pixmap(dpi=ocr_dpi)
            img = np.frombuffer(pix.samples, dtype=np.uint8)
            channels = pix.n
            img = img.reshape((pix.height, pix.width, channels))

            # RapidOCR returns a list of detections and elapsed time.
            result, _ = ocr_engine(img)
            if not result:
                continue

            lines = [item[1] for item in result if item and len(item) > 1 and item[1]]
            page_text = "\n".join(lines).strip()
            if not page_text:
                continue

            ocr_docs.append(
                Document(
                    page_content=page_text,
                    metadata={"source": str(pdf_path), "page": page_idx}
                )
            )
    return ocr_docs

# Step 1: Load all PDFs from the docs folder
print("Loading PDFs...")
documents = []
ocr_engine = RapidOCR()
ocr_dpi = int(os.getenv("OCR_DPI", "150"))
ocr_max_pages_raw = os.getenv("OCR_MAX_PAGES", "")
ocr_max_pages = int(ocr_max_pages_raw) if ocr_max_pages_raw.strip() else None

if ocr_max_pages:
    print(f"OCR page limit enabled: {ocr_max_pages} pages per PDF")
print(f"OCR DPI: {ocr_dpi}")

for pdf_path in Path("docs").glob("*.pdf"):
    print(f"Loading {pdf_path.name}...")
    pdf_docs = load_documents_with_text(pdf_path)
    non_empty_pdf_docs = [d for d in pdf_docs if d.page_content and d.page_content.strip()]

    if non_empty_pdf_docs:
        print(f"  extracted text pages: {len(non_empty_pdf_docs)}")
        documents.extend(non_empty_pdf_docs)
        continue

    print("  no selectable text found; running OCR...")
    ocr_docs = load_documents_with_ocr(pdf_path, ocr_engine, ocr_dpi=ocr_dpi, max_pages=ocr_max_pages)
    print(f"  OCR text pages: {len(ocr_docs)}")
    documents.extend(ocr_docs)
print(f"Loaded {len(documents)} pages")

# Step 2: Split into chunks
print("Splitting into chunks...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# Chroma cannot upsert empty embeddings; skip blank chunks.
valid_chunks = [c for c in chunks if c.page_content and c.page_content.strip()]
print(f"Kept {len(valid_chunks)} non-empty chunks")

if not valid_chunks:
    raise ValueError(
        "No text was extracted from PDFs after standard parsing and OCR. "
        "Check PDF quality and OCR dependencies."
    )

# Step 3: Convert to vectors and store
print("Creating vector database...")
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma.from_documents(
    documents=valid_chunks,
    embedding=embedding,
    persist_directory="vectorstore"
)
print("Done! Vector database saved.")
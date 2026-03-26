"""Configuration management for the Petroleum AI application."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration from environment variables."""

    # Google API Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_MODEL: str = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")

    # Vector Database Configuration
    VECTORSTORE_PATH: str = os.getenv("VECTORSTORE_PATH", "vectorstore")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # LLM Configuration
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "3"))

    # OCR Configuration
    OCR_DPI: int = int(os.getenv("OCR_DPI", "150"))
    OCR_MAX_PAGES: Optional[int] = (
        int(ocr_pages) if (ocr_pages := os.getenv("OCR_MAX_PAGES", "")) else None
    )

    # Document Processing
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    DOCS_PATH: str = os.getenv("DOCS_PATH", "docs")

    # Gradio Configuration
    GRADIO_PORT: int = int(os.getenv("GRADIO_PORT", "7860"))
    GRADIO_SHARE: bool = os.getenv("GRADIO_SHARE", "false").lower() == "true"

    @classmethod
    def validate(cls) -> None:
        """Validate required configuration values.

        Raises:
            ValueError: If critical configuration is missing.
        """
        if not cls.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is not set. "
                "Please set it in .env file or as an environment variable."
            )


# Example environment variables for reference
"""
# .env file example:
GOOGLE_API_KEY=your_api_key_here
GOOGLE_MODEL=gemini-2.5-flash
VECTORSTORE_PATH=vectorstore
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_TEMPERATURE=0.3
TOP_K_RESULTS=3
OCR_DPI=150
OCR_MAX_PAGES=
CHUNK_SIZE=500
CHUNK_OVERLAP=50
DOCS_PATH=docs
GRADIO_PORT=7860
GRADIO_SHARE=false
"""

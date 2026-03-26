"""Utility functions and logging setup for the Petroleum AI application."""

import logging
import sys
from typing import List
from langchain_core.documents import Document


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("petroleum_ai")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger


def format_documents(documents: List[Document]) -> str:
    """Format a list of documents into a single string for context.

    Args:
        documents: List of Document objects from LangChain.

    Returns:
        Formatted string with document contents separated by double newlines.
    """
    return "\n\n".join(doc.page_content for doc in documents)


def extract_sources(documents: List[Document]) -> set:
    """Extract unique source documents from a list of documents.

    Args:
        documents: List of Document objects from LangChain.

    Returns:
        Set of unique source file paths.
    """
    return set(doc.metadata.get("source", "unknown") for doc in documents)


def format_sources(sources: set) -> str:
    """Format sources into a readable string.

    Args:
        sources: Set of source file paths.

    Returns:
        Formatted sources string.
    """
    if not sources:
        return "No sources available"
    source_list = sorted(sources)
    return ", ".join(f"📄 {source.split('/')[-1]}" for source in source_list)

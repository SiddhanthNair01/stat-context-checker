import re
import trafilatura
import pdfplumber


def text_from_url(url: str) -> dict:
    """Download a web page and return its main article text plus metadata."""
    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        raise ValueError("Could not download that page. Try pasting the text instead.")
    text = trafilatura.extract(downloaded, include_tables=True, include_comments=False)
    if not text:
        raise ValueError("No article text found (paywall or JavaScript-only page?).")
    meta = trafilatura.extract_metadata(downloaded)
    return {
        "text": text,
        "title": meta.title if meta else None,
        "date": meta.date if meta else None,
        "source": url,
    }


def text_from_pdf(file) -> dict:
    """Accepts a file path or an uploaded file object."""
    pages = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    text = "\n".join(pages)
    if len(text.strip()) < 50:
        raise ValueError("This PDF looks scanned (no text layer).")
    return {"text": text, "title": None, "date": None, "source": "uploaded PDF"}


def split_sentences(text: str) -> list[str]:
    """Simple splitter for now; Phase 6 replaces it with spaCy."""
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", text)
    return [p.strip() for p in parts if len(p.strip()) > 20]
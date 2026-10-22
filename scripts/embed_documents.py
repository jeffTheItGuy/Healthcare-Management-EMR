#!/usr/bin/env python3
"""
One-off script to ingest PDFs into pgvector.
Usage:
    python scripts/embed_documents.py --file guidelines/malaria.pdf --type GUIDELINE
"""
import argparse
import hashlib
import os
import re
from pathlib import Path

import PyPDF2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.database import Base
from app.models.semantic import ClinicalDocumentSource, ClinicalDocumentChunk
from app.services.embedding_service import get_embedding

settings = get_settings()
engine = create_engine(settings.database_url)
Session = sessionmaker(bind=engine)

CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    for i in range(0, len(words), size - overlap):
        chunk = " ".join(words[i : i + size])
        chunks.append(chunk)
    return chunks

def extract_text_from_pdf(path: str) -> str:
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    text = re.sub(r"\s+", " ", text).strip()
    return text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to PDF file")
    parser.add_argument("--type", default="GUIDELINE", help="GUIDELINE, PROTOCOL, SOP, etc.")
    parser.add_argument("--title", default=None, help="Override document title")
    args = parser.parse_args()

    db = Session()
    try:
        with open(args.file, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        existing = db.query(ClinicalDocumentSource).filter_by(file_hash=file_hash).first()
        if existing:
            print(f"Already ingested: {existing.source_id}")
            return

        text = extract_text_from_pdf(args.file)
        if not text:
            print("No text extracted from PDF.")
            return

        title = args.title or Path(args.file).stem.replace("_", " ").title()

        source = ClinicalDocumentSource(
            source_title=title,
            source_type=args.type,
            document_url=str(Path(args.file).resolve()),
            file_hash=file_hash,
            page_count=0,
            ingest_status="PROCESSING",
        )
        db.add(source)
        db.flush()

        chunks = chunk_text(text)
        print(f"Creating {len(chunks)} chunks...")

        for idx, chunk_text_str in enumerate(chunks):
            embedding = get_embedding(chunk_text_str)
            chunk = ClinicalDocumentChunk(
                source_id=source.source_id,
                chunk_index=idx,
                chunk_text=chunk_text_str,
                chunk_text_embedding=embedding.tolist(),
                token_count=len(chunk_text_str.split()),
            )
            db.add(chunk)

        source.ingest_status = "COMPLETED"
        db.commit()
        print(f"Ingested {len(chunks)} chunks for source: {source.source_id}")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()

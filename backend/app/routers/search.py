from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import List, Optional

from app.database import get_db
from app.services.embedding_service import get_embedding
from app.models.semantic import SearchQuery

router = APIRouter()

class DocumentSearchRequest(BaseModel):
    query: str
    top_k: int = 5
    source_types: Optional[List[str]] = None

class DocumentSearchResult(BaseModel):
    chunk_text: str
    similarity: float
    source_title: str
    source_type: str

@router.post("/documents", response_model=List[DocumentSearchResult])
def search_documents(req: DocumentSearchRequest, db: Session = Depends(get_db)):
    """Semantic search over clinical guidelines and protocols."""
    embedding = get_embedding(req.query)

    query_log = SearchQuery(
        query_text=req.query,
        query_embedding=embedding.tolist(),
        search_target="DOCUMENTS",
        top_k=req.top_k,
    )
    db.add(query_log)

    sql = """
    SELECT
        c.chunk_text,
        1 - (c.chunk_text_embedding <=> :embedding) AS similarity,
        s.source_title,
        s.source_type
    FROM clinical_document_chunks c
    JOIN clinical_document_sources s ON c.source_id = s.source_id
    WHERE s.is_active = TRUE
    """
    params = {"embedding": str(embedding.tolist())}

    if req.source_types:
        placeholders = ", ".join([f":st{i}" for i in range(len(req.source_types))])
        sql += f" AND s.source_type IN ({placeholders})"
        for i, st in enumerate(req.source_types):
            params[f"st{i}"] = st

    sql += """
    ORDER BY c.chunk_text_embedding <=> :embedding
    LIMIT :top_k
    """
    params["top_k"] = req.top_k

    results = db.execute(text(sql), params).mappings().all()

    query_log.result_count = len(results)
    query_log.results = [dict(r) for r in results]
    db.commit()

    return [
        DocumentSearchResult(
            chunk_text=r["chunk_text"],
            similarity=round(float(r["similarity"]), 4),
            source_title=r["source_title"],
            source_type=r["source_type"],
        )
        for r in results
    ]


class PatientSimilarityRequest(BaseModel):
    patient_id: str
    top_k: int = 5

class PatientSimilarityResult(BaseModel):
    patient_id: str
    similarity: float
    embedding_type: str

@router.post("/patients/similar", response_model=List[PatientSimilarityResult])
def find_similar_patients(req: PatientSimilarityRequest, db: Session = Depends(get_db)):
    """Find patients with similar clinical profiles."""
    sql = """
    SELECT embedding_vector
    FROM patient_clinical_embeddings
    WHERE patient_id = :pid
    ORDER BY generated_at DESC
    LIMIT 1
    """
    row = db.execute(text(sql), {"pid": req.patient_id}).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="No embedding found for this patient")

    embedding = row[0]

    sql = """
    SELECT
        patient_id,
        1 - (embedding_vector <=> :embedding) AS similarity,
        embedding_type
    FROM patient_clinical_embeddings
    WHERE patient_id != :pid
    ORDER BY embedding_vector <=> :embedding
    LIMIT :top_k
    """
    results = db.execute(
        text(sql), {"embedding": str(embedding.tolist()), "pid": req.patient_id, "top_k": req.top_k}
    ).mappings().all()

    return [
        PatientSimilarityResult(
            patient_id=str(r["patient_id"]),
            similarity=round(float(r["similarity"]), 4),
            embedding_type=r["embedding_type"],
        )
        for r in results
    ]
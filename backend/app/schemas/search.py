from typing import List, Optional
from pydantic import BaseModel


class DocumentSearchRequest(BaseModel):
    query: str
    top_k: int = 5
    source_types: Optional[List[str]] = None


class DocumentSearchResult(BaseModel):
    chunk_text: str
    similarity: float
    source_title: str
    source_type: str


class PatientSimilarityRequest(BaseModel):
    patient_id: str
    top_k: int = 5


class PatientSimilarityResult(BaseModel):
    patient_id: str
    similarity: float
    embedding_type: str
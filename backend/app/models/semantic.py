import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, JSON, ARRAY, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.sql import func
from app.database import Base


class ClinicalDocumentSource(Base):
    __tablename__ = "clinical_document_sources"

    source_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_title = Column(String(500), nullable=False)
    source_type = Column(String(50), nullable=False, default="GUIDELINE")
    document_url = Column(String(1000))
    file_hash = Column(String(64))
    page_count = Column(Integer)
    language = Column(String(10), default="en")
    specialty_tags = Column(ARRAY(String))
    ingest_status = Column(String(20), default="PENDING")
    is_active = Column(Boolean, default=True)
    ingested_by = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"))
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ClinicalDocumentChunk(Base):
    __tablename__ = "clinical_document_chunks"

    chunk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("clinical_document_sources.source_id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_text_embedding = Column(Vector(384))
    chunk_metadata = Column(JSON)
    token_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PatientClinicalEmbedding(Base):
    __tablename__ = "patient_clinical_embeddings"

    embedding_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    record_id = Column(UUID(as_uuid=True), ForeignKey("medical_records.record_id"), nullable=False)
    embedding_type = Column(String(50), nullable=False, default="RECORD_SUMMARY")
    embedding_text = Column(Text, nullable=False)
    embedding_vector = Column(Vector(384))
    model_name = Column(String(50))
    model_version = Column(String(20))
    generated_at = Column(DateTime(timezone=True), server_default=func.now())


class SearchQuery(Base):
    __tablename__ = "search_queries"

    query_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    queried_by_staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"))
    query_text = Column(Text, nullable=False)
    query_embedding = Column(Vector(384))
    search_target = Column(String(20), default="DOCUMENTS")
    filters = Column(JSON)
    top_k = Column(Integer, default=10)
    similarity_threshold = Column(Numeric(3, 2), default=0.70)
    results = Column(JSON)
    result_count = Column(Integer)
    execution_time_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
-- ============================================================
-- EMR — PGVECTOR HELPER FUNCTIONS & CONFIG
-- Run after 04_indexes.sql (or any time after pgvector is ready)
-- ============================================================

-- --------------------------------------------------------------
-- 1. JSONB indexes for metadata filtering (used by semantic search)
-- --------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_document_chunks_metadata
ON clinical_document_chunks USING GIN (chunk_metadata);

CREATE INDEX IF NOT EXISTS idx_search_queries_filters
ON search_queries USING GIN (filters);

CREATE INDEX IF NOT EXISTS idx_document_sources_tags
ON clinical_document_sources USING GIN (specialty_tags);

-- --------------------------------------------------------------
-- 2. Semantic search over clinical documents
-- --------------------------------------------------------------
CREATE OR REPLACE FUNCTION search_clinical_documents(
    query_embedding vector(384),
    match_threshold float DEFAULT 0.70,
    match_count int DEFAULT 10,
    filter_source_types text[] DEFAULT NULL
)
RETURNS TABLE(
    chunk_id uuid,
    chunk_text text,
    similarity float,
    source_id uuid,
    source_title varchar(500),
    source_type varchar(50),
    chunk_index int,
    chunk_metadata jsonb
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.chunk_id,
        c.chunk_text,
        1 - (c.chunk_text_embedding <=> query_embedding)::float AS similarity,
        s.source_id,
        s.source_title,
        s.source_type,
        c.chunk_index,
        c.chunk_metadata
    FROM clinical_document_chunks c
    JOIN clinical_document_sources s ON c.source_id = s.source_id
    WHERE s.is_active = TRUE
      AND s.ingest_status = 'COMPLETED'
      AND 1 - (c.chunk_text_embedding <=> query_embedding) >= match_threshold
      AND (filter_source_types IS NULL OR s.source_type = ANY(filter_source_types))
    ORDER BY c.chunk_text_embedding <=> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION search_clinical_documents IS
'Performs cosine-similarity search over chunked clinical documents. Returns results above match_threshold ordered by similarity.';

-- --------------------------------------------------------------
-- 3. Find patients with similar clinical profiles
-- --------------------------------------------------------------
CREATE OR REPLACE FUNCTION find_similar_patients(
    target_patient_id uuid,
    match_count int DEFAULT 5,
    embedding_filter varchar(50) DEFAULT 'FULL_HISTORY'
)
RETURNS TABLE(
    patient_id uuid,
    similarity float,
    embedding_type varchar(50),
    generated_at timestamptz
) AS $$
DECLARE
    target_embedding vector(384);
BEGIN
    SELECT pce.embedding_vector INTO target_embedding
    FROM patient_clinical_embeddings pce
    WHERE pce.patient_id = target_patient_id
      AND pce.embedding_type = COALESCE(embedding_filter, 'FULL_HISTORY')
    ORDER BY pce.generated_at DESC
    LIMIT 1;

    IF target_embedding IS NULL THEN
        RETURN;
    END IF;

    RETURN QUERY
    SELECT 
        pce.patient_id,
        1 - (pce.embedding_vector <=> target_embedding)::float AS similarity,
        pce.embedding_type,
        pce.generated_at
    FROM patient_clinical_embeddings pce
    WHERE pce.patient_id != target_patient_id
      AND pce.embedding_type = COALESCE(embedding_filter, 'FULL_HISTORY')
    ORDER BY pce.embedding_vector <=> target_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION find_similar_patients IS
'Finds patients with similar clinical embeddings using cosine distance. Defaults to FULL_HISTORY embeddings.';

-- --------------------------------------------------------------
-- 4. Log a semantic search query (used by application layer)
-- --------------------------------------------------------------
CREATE OR REPLACE FUNCTION log_search_query(
    p_queried_by_staff_id uuid,
    p_query_text text,
    p_query_embedding vector(384),
    p_search_target varchar(20) DEFAULT 'DOCUMENTS',
    p_filters jsonb DEFAULT NULL,
    p_top_k int DEFAULT 10,
    p_similarity_threshold decimal(3,2) DEFAULT 0.70,
    p_results jsonb DEFAULT NULL,
    p_result_count int DEFAULT NULL,
    p_execution_time_ms int DEFAULT NULL
)
RETURNS uuid AS $$
DECLARE
    new_query_id uuid;
BEGIN
    INSERT INTO search_queries (
        queried_by_staff_id,
        query_text,
        query_embedding,
        search_target,
        filters,
        top_k,
        similarity_threshold,
        results,
        result_count,
        execution_time_ms
    ) VALUES (
        p_queried_by_staff_id,
        p_query_text,
        p_query_embedding,
        p_search_target,
        p_filters,
        p_top_k,
        p_similarity_threshold,
        p_results,
        p_result_count,
        p_execution_time_ms
    )
    RETURNING query_id INTO new_query_id;

    RETURN new_query_id;
END;
$$ LANGUAGE plpgsql;

-- --------------------------------------------------------------
-- 5. Embedding statistics dashboard helper
-- --------------------------------------------------------------
CREATE OR REPLACE FUNCTION get_embedding_stats()
RETURNS TABLE(
    total_document_chunks bigint,
    total_document_sources bigint,
    total_patient_embeddings bigint,
    total_search_queries bigint,
    avg_chunk_tokens numeric,
    latest_embedding_at timestamptz
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT COUNT(*) FROM clinical_document_chunks),
        (SELECT COUNT(*) FROM clinical_document_sources),
        (SELECT COUNT(*) FROM patient_clinical_embeddings),
        (SELECT COUNT(*) FROM search_queries),
        (SELECT ROUND(AVG(token_count)::numeric, 2) FROM clinical_document_chunks WHERE token_count IS NOT NULL),
        (SELECT MAX(generated_at) FROM patient_clinical_embeddings);
END;
$$ LANGUAGE plpgsql STABLE;

-- --------------------------------------------------------------
-- 6. Trigger: auto-update ingest_status timestamp
-- --------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_source_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_source_timestamp ON clinical_document_sources;
CREATE TRIGGER trg_update_source_timestamp
    BEFORE UPDATE ON clinical_document_sources
    FOR EACH ROW
    EXECUTE FUNCTION update_source_timestamp();

-- --------------------------------------------------------------
-- 7. Grant execute permissions
-- --------------------------------------------------------------
GRANT EXECUTE ON FUNCTION search_clinical_documents TO emr_staff;
GRANT EXECUTE ON FUNCTION search_clinical_documents TO emr_admin;
GRANT EXECUTE ON FUNCTION find_similar_patients TO emr_staff;
GRANT EXECUTE ON FUNCTION find_similar_patients TO emr_admin;
GRANT EXECUTE ON FUNCTION log_search_query TO emr_staff;
GRANT EXECUTE ON FUNCTION log_search_query TO emr_admin;
GRANT EXECUTE ON FUNCTION get_embedding_stats TO emr_admin;

-- --------------------------------------------------------------
-- 8. pgvector performance tuning (session-level guidance)
-- --------------------------------------------------------------
-- For large-scale production workloads, consider:
--   SET hnsw.ef_search = 100;  -- higher = more accurate, slower
--   SET work_mem = '256MB';    -- helps with large vector sorts
--
-- These are typically set per-connection by the application or
-- in postgresql.conf rather than here.
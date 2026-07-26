export interface DocumentSearchRequest {
  query: string;
  top_k?: number;
  source_types?: string[];
}

export interface DocumentSearchResult {
  chunk_text: string;
  similarity: number;
  source_title: string;
  source_type: string;
}

export interface PatientSimilarityRequest {
  patient_id: string;
  top_k?: number;
}

export interface PatientSimilarityResult {
  patient_id: string;
  similarity: number;
  embedding_type: string;
}

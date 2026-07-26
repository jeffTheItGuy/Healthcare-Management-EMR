"""Tests for semantic search endpoints."""

import numpy as np
from unittest.mock import patch, MagicMock
from uuid import uuid4


class TestDocumentSearch:
    def test_search_documents_success(self, client, db):
        """Test successful semantic search over clinical documents."""
        mock_embedding = np.array([0.1] * 384, dtype=np.float32)

        with patch("app.routers.search.get_embedding", return_value=mock_embedding):
            mock_result = MagicMock()
            mock_result.mappings.return_value.all.return_value = [
                {
                    "chunk_text": "Diabetes management protocol",
                    "similarity": 0.95,
                    "source_title": "Clinical Guidelines 2024",
                    "source_type": "GUIDELINE",
                }
            ]

            original_execute = db.execute

            def side_effect_execute(*args, **kwargs):
                sql_str = str(args[0]) if args else ""
                if "clinical_document_chunks" in sql_str:
                    return mock_result
                return original_execute(*args, **kwargs)

            with patch.object(db, "execute", side_effect=side_effect_execute):
                response = client.post(
                    "/search/documents",
                    json={"query": "diabetes treatment", "top_k": 5},
                )
                assert response.status_code == 200
                data = response.json()
                assert len(data) == 1
                assert data[0]["chunk_text"] == "Diabetes management protocol"
                assert data[0]["similarity"] == 0.95
                assert data[0]["source_type"] == "GUIDELINE"

    def test_search_documents_with_source_filter(self, client, db):
        """Test document search filtered by source type."""
        mock_embedding = np.array([0.1] * 384, dtype=np.float32)

        with patch("app.routers.search.get_embedding", return_value=mock_embedding):
            mock_result = MagicMock()
            mock_result.mappings.return_value.all.return_value = []

            original_execute = db.execute

            def side_effect_execute(*args, **kwargs):
                sql_str = str(args[0]) if args else ""
                if "clinical_document_chunks" in sql_str:
                    # Assert that source type placeholders are rendered
                    assert any(f":st{i}" in sql_str for i in range(2))
                    return mock_result
                return original_execute(*args, **kwargs)

            with patch.object(db, "execute", side_effect=side_effect_execute):
                response = client.post(
                    "/search/documents",
                    json={
                        "query": "hypertension",
                        "top_k": 3,
                        "source_types": ["GUIDELINE", "PROTOCOL"],
                    },
                )
                assert response.status_code == 200
                assert response.json() == []


class TestPatientSimilarity:
    def test_find_similar_patients(self, client, db):
        """Test finding patients with similar clinical profiles."""
        mock_embedding = np.array([0.2] * 384, dtype=np.float32)

        fetchone_result = MagicMock()
        fetchone_result.fetchone.return_value = ([0.2] * 384,)

        similar_result = MagicMock()
        similar_result.mappings.return_value.all.return_value = [
            {
                "patient_id": uuid4(),
                "similarity": 0.88,
                "embedding_type": "RECORD_SUMMARY",
            }
        ]

        original_execute = db.execute

        def side_effect_execute(*args, **kwargs):
            sql_str = str(args[0]) if args else ""
            if "patient_clinical_embeddings" in sql_str and "LIMIT 1" in sql_str:
                return fetchone_result
            elif "patient_clinical_embeddings" in sql_str:
                return similar_result
            return original_execute(*args, **kwargs)

        with patch.object(db, "execute", side_effect=side_effect_execute):
            response = client.post(
                "/search/patients/similar",
                json={"patient_id": str(uuid4()), "top_k": 5},
            )
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["similarity"] == 0.88
            assert data[0]["embedding_type"] == "RECORD_SUMMARY"

    def test_find_similar_patients_no_embedding(self, client, db):
        """Test 404 response when patient has no clinical embedding."""
        mock_result = MagicMock()
        mock_result.fetchone.return_value = None

        original_execute = db.execute

        def side_effect_execute(*args, **kwargs):
            sql_str = str(args[0]) if args else ""
            if "patient_clinical_embeddings" in sql_str:
                return mock_result
            return original_execute(*args, **kwargs)

        with patch.object(db, "execute", side_effect=side_effect_execute):
            response = client.post(
                "/search/patients/similar",
                json={"patient_id": str(uuid4()), "top_k": 5},
            )
            assert response.status_code == 404
            assert "No embedding found" in response.json()["detail"]
# ZimEMR — Zimbabwe Hospital Management System

A production-ready Electronic Medical Records (EMR) system built for Zimbabwean healthcare facilities. Features multi-currency billing (USD/ZiG), batch-tracked pharmacy inventory, critical lab alerting, and local semantic search via pgvector — no cloud AI required.

## Stack

| Layer | Tech |
|---|---|
| **Backend** | Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic |
| **Frontend** | Angular 17, Angular Material |
| **Database** | PostgreSQL 16 + pgvector |
| **Search** | Local embeddings (all-MiniLM-L6-v2, 384-dim) via sentence-transformers |
| **Deploy** | Docker Compose (dev), Docker Compose + Nginx (prod) |

## Quick Start

```bash
# 1. Clone
git clone https://github.com/yourorg/zim-emr.git && cd zim-emr

# 2. Environment
cp .env.example .env
# Edit .env with your DB credentials and JWT secret

# 3. Run
docker compose up --build

# 4. Access
# API Docs:  http://localhost:8000/docs
# Frontend: http://localhost:4200
# Enterprise-IT-Support-AI# Enterprise IT Support AI — InvoiceFlow-style organization

Reorganized from the uploaded **Enterprise IT Support Agentic RAG Copilot** source. Core graph behavior and original frontend are retained, with fewer nested folders and numbered code sections.

## Architecture

START → route_question → [direct_answer OR retrieve_kb → grade_kb → (generate_from_kb OR search_web → grade_web → (generate_from_web OR rewrite_query → retrieve_kb OR insufficient))] → END

The agent first tries company KB in Pinecone, then Tavily if evidence is weak. Rewrites and retries up to MAX_RETRIES. Documents are chunked and embedded into Pinecone. SQLite stores question, source, and trace.

## Windows CMD setup

```cmd
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env
python template.py
python app.py
```

Open http://127.0.0.1:8080 . Set OPENAI_API_KEY, TAVILY_API_KEY, PINECONE_API_KEY and a secure ADMIN_API_KEY in `.env` first.

## Initial KB indexing

```cmd
python ingest_sample_kb.py
```

## Tests

```cmd
python -m pytest tests -q
```

Install pytest separately if needed: `pip install pytest`.

## Endpoints

- `GET /` frontend
- `GET /api/health` health check
- `POST /api/chat` JSON `{"question":"How do I connect to VPN?"}`
- `POST /api/ingest` multipart `file` with `X-Admin-Key` header (PDF/DOCX/TXT/MD, max 10MB)

## Important

- Never commit `.env`. Uploaded documents are removed from local uploads after indexing.
- Pinecone indexes are **never automatically deleted** for embedding-dimension mismatch; choose a compatible model or create a separate index.
- The original SQLite audit log is application-wide; this is **not a multi-user privacy or authentication system**. Add per-user authorization and separate audit access before public production deployment.
- External APIs require valid keys and network connectivity. Tests supplied here validate structure and syntax, not live end-to-end API behavior.
- The existing frontend and its API contracts are retained.

# ==========================================
# SECTION 1: IMPORTS
# ==========================================
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Request
from pydantic import BaseModel, Field
from config import get_settings
from backend import run_it_support_agent
from tools.pinecone_tool import add_documents 
from tools.document_loader import load_file, SUPPORTED
from tools.document_chunker import chunk_documents
from tools.audit_tool import write_audit, init_db

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# ==========================================
# SECTION 2: FASTAPI CONFIGURATION
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
settings = get_settings()
init_db()
app = FastAPI(title=settings.app_name, version="1.0.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "app_name": settings.app_name})


# ==========================================
# SECTION 3: REQUEST MODEL
# ==========================================
class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=3000)


# ==========================================
# SECTION 4: HEALTH AND CHAT ENDPOINTS
# ==========================================
@app.get("/api/health")
def health():
    return {"status": "ok", "service": settings.app_name}


@app.post("/api/chat")
def chat(payload: ChatRequest):
    try:
        result = run_it_support_agent(payload.question)
        write_audit(payload.question, result["source_used"], result.get("trace", []))

        return {
            "answer": result["answer"],
            "source_used": result["source_used"],
            "trace": result.get("trace", []),
            "citations": result.get("citations", []),
            "rewritten_query": result.get("current_query", payload.question),

        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc



# ==========================================
# SECTION 5: DOCUMENT INGESTION ENDPOINT
# ==========================================
@app.post("/api/ingest")
async def ingest(file: UploadFile = File(...), x_admin_key: str = Header(default="")):
    if not settings.admin_api_key or settings.admin_api_key == "change-me" or x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=401, detail="Invalid admin key")
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in SUPPORTED:
        raise HTTPException(status_code=400, detail=f"Supported: {', '.join(sorted(SUPPORTED))}")
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    dest = upload_dir / Path(file.filename).name
    content = await file.read(10 * 1024 * 1024 + 1)
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Maximum file size is 10 MB")
    dest.write_bytes(content)
    try:
        docs = load_file(dest)
        chunks = chunk_documents(docs)
        ids = add_documents(chunks)
        return {"message": "Document indexed", "file": dest.name, "chunks": len(chunks), "ids_created": len(ids)}
    finally:
        dest.unlink(missing_ok=True)


# ==========================================
# SECTION 6: RUN FASTAPI SERVER
# ==========================================
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)

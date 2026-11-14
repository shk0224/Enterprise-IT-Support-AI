# ==========================================
# SECTION 1: IMPORTS
# ==========================================
import json
import sqlite3
from datetime import datetime, timezone
from config import get_settings

settings = get_settings()

# ==========================================
# SECTION 2: INITIALIZE AUDIT DATABASE
# ==========================================
def init_db() -> None:
    from pathlib import Path
    Path(settings.audit_db_path).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(settings.audit_db_path)
    con.execute(
        """CREATE TABLE IF NOT EXISTS query_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            question TEXT NOT NULL,
            source_used TEXT NOT NULL,
            trace_json TEXT NOT NULL
        )"""
    )
    con.commit()
    con.close()

# ==========================================
# SECTION 3: SAVE AUDIT RECORD
# ==========================================
def write_audit(question: str, source_used: str, trace: list[str]) -> None:
    from pathlib import Path
    Path(settings.audit_db_path).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(settings.audit_db_path)
    con.execute(
        "INSERT INTO query_audit(created_at, question, source_used, trace_json) VALUES (?, ?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), question, source_used, json.dumps(trace)),
    )
    con.commit()
    con.close()

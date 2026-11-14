from pathlib import Path

# ==========================================
# SECTION 1: PROJECT ROOT
# ==========================================
PROJECT_ROOT = Path(__file__).resolve().parent

# ==========================================
# SECTION 2: FOLDER AND FILE LISTS
# ==========================================
folders = ["tools", "templates", "static", "data", "data/sample_kb", "uploads", "tests"]

files = [
    "app.py", "backend.py", "config.py", "template.py",
    "requirements.txt", ".env.example", ".gitignore", "README.md", "Dockerfile",
    "tools/__init__.py", "tools/document_loader.py", "tools/document_chunker.py",
    "tools/pinecone_tool.py", "tools/web_search_tool.py", "tools/audit_tool.py",
    "templates/index.html", "static/style.css", "static/app.js",
    "data/sample_kb/company_it_handbook.md", "data/sample_kb/service_desk_runbook.md",
    "uploads/.gitkeep", "tests/test_structure.py",
]

# ==========================================
# SECTION 3: CREATE FOLDERS
# ==========================================
for folder in folders:
    folder_path = PROJECT_ROOT / folder
    folder_path.mkdir(parents=True, exist_ok=True)
    print(f"Folder ready: {folder_path}")

# ==========================================
# SECTION 4: CREATE FILES
# ==========================================
for file in files:
    file_path = PROJECT_ROOT / file
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch(exist_ok=True)
    print(f"File ready: {file_path}")

print("Project structure created successfully.")

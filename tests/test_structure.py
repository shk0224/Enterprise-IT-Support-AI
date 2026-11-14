from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]

def test_python_syntax():
    for path in [ROOT / "app.py", ROOT / "backend.py", ROOT / "config.py", *(ROOT / "tools").glob("*.py")]:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

def test_frontend_files():
    for name in ("templates/index.html", "static/style.css", "static/app.js"):
        assert (ROOT / name).is_file()

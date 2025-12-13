from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TOKEN = (BASE_DIR / "TOKEN").read_text().strip()

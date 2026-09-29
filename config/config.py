from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

AI_BASE_URL = os.getenv("AI_BASE_URL", "").strip()
AI_API_KEY = os.getenv("AI_API_KEY", "").strip()
AI_MODEL = os.getenv("AI_MODEL", "").strip()

MEMORY_DIR = ROOT / "data" / "memory"
LOG_DIR = ROOT / "logs"
BACKUP_DIR = ROOT / "backups"
SANDBOX_DIR = ROOT / "sandbox"

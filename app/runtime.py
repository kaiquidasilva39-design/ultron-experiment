import os
from datetime import datetime, timezone

from config.config import ROOT
from app.state import save


def runtime_info():
    return {
        "agent": os.getenv("AGENT_NAME", "ULTRON-EXPERIMENT"),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "root": str(ROOT),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def checkpoint():
    info = runtime_info()
    save({
        "runtime": info,
        "checkpoint": True,
    })
    return info

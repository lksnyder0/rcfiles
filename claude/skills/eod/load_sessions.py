#!/usr/bin/env python3
"""Load and filter Claude Code session index files for a given date.

Usage: python3 load_sessions.py [YYYY-MM-DD]
       Defaults to today's date if omitted.

Output: JSON array of matching session objects to stdout.
"""

import json
import sys
from datetime import date
from pathlib import Path

INDEX_DIR = Path.home() / ".claude" / "session-index"


def load_sessions(target_date: str) -> list[dict]:
    if not INDEX_DIR.is_dir():
        return []

    sessions = []
    for path in INDEX_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        days_active = data.get("days_active", [])
        started = (data.get("started_at") or "")[:10]
        ended = (data.get("ended_at") or "")[:10]

        if target_date in days_active or started == target_date or ended == target_date:
            sessions.append(data)

    return sessions


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    print(json.dumps(load_sessions(target), indent=2))

"""CLI for screening building retrofit records."""
import json
import sys
from pathlib import Path
from .assessment import rank_retrofits

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 -m core.cli <records.json>")
        return 2
    path = Path(sys.argv[1])
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        records = payload if isinstance(payload, list) else payload.get("buildings", [])
        if not isinstance(records, list):
            raise ValueError("JSON must be a list or an object with a 'buildings' list.")
        print(json.dumps(rank_retrofits(records), indent=2))
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())

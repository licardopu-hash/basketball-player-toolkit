"""Command-line interface: python -m basketball_toolkit input.csv."""
import csv
import json
import sys
from .stats import summarize_games

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m basketball_toolkit <games.csv>", file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], newline="", encoding="utf-8-sig") as f:
            output = summarize_games(csv.DictReader(f))
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Reset Handover database from the Riverside fixture."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from server.ledger import CaseStore
from server.paths import DEFAULT_DB


def main() -> None:
    db = DEFAULT_DB
    if db.exists():
        db.unlink()
    store = CaseStore(db)
    store.init_schema()
    store.reset_from_fixture()
    print(f"Reset complete: {db}")


if __name__ == "__main__":
    main()

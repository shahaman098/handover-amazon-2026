#!/usr/bin/env python3
"""End-to-end verification: reset, correction loop, stale proposal, persistence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from server.ledger import CaseStore, LedgerError
from server.paths import DEFAULT_DB


def main() -> int:
    db = DEFAULT_DB
    if db.exists():
        db.unlink()

    store = CaseStore(db)
    store.init_schema()
    store.reset_from_fixture()

    prop = store.propose_income_correction("adviser")
    store.confirm_proposal(prop["proposal_id"], "applicant")

    try:
        store.propose_income_correction("adviser", expected_revision=0)
        print("FAIL: stale revision proposal should be rejected")
        return 1
    except LedgerError as e:
        if e.code != "stale_revision":
            print("FAIL: wrong error", e.code)
            return 1

    try:
        store.confirm_proposal(prop["proposal_id"], "applicant")
        print("FAIL: duplicate confirm should be rejected")
        return 1
    except LedgerError as e:
        if e.code != "invalid":
            print("FAIL: wrong duplicate error", e.code)
            return 1

    prop2 = store.propose_income_correction("adviser", custom_income="2380")
    store.confirm_proposal(prop2["proposal_id"], "applicant")
    view = store.get_case_view()
    if view["assessments"][0]["value"] != "2380":
        print("FAIL: custom income not applied")
        return 1

    rev = view["case_revision"]
    store2 = CaseStore(db)
    view2 = store2.get_case_view()
    if view2["case_revision"] != rev:
        print("FAIL: persistence")
        return 1

    ok, _ = store.try_cycle_edge()
    if ok:
        print("FAIL: cycle detection")
        return 1

    print("VERIFICATION PASSED")
    print(json.dumps({"case_revision": rev, "ledger_events": len(view2["ledger_tail"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

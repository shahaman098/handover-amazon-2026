#!/usr/bin/env python3
"""Independent verification against fixtures/case_riverside/expected.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from server.ledger import CaseStore
from server.paths import DEFAULT_DB, FIXTURE_CASE


def main() -> int:
    expected_path = FIXTURE_CASE / "expected.json"
    expected = json.loads(expected_path.read_text())
    exp = expected["after_payslip_correction"]

    if DEFAULT_DB.exists():
        DEFAULT_DB.unlink()
    store = CaseStore(DEFAULT_DB)
    store.init_schema()
    store.reset_from_fixture()
    prop = store.propose_income_correction("adviser")
    store.confirm_proposal(prop["proposal_id"], "applicant")
    view = store.get_case_view()

    failures: list[str] = []

    def asm(aid: str):
        for a in view["assessments"]:
            if a["id"] == aid:
                return a
        return None

    a1 = asm("A1")
    a2 = asm("A2")
    a3 = asm("A3")

    if a1 and a1["value"] != exp["A1_value"]:
        failures.append(f"A1 value {a1['value']} != expected {exp['A1_value']}")
    if a2 and a2["value"] != exp["A2_value"]:
        failures.append(f"A2 value {a2['value']} != expected {exp['A2_value']}")
    if a3 and a3["status"] != exp["A3_status"]:
        failures.append(f"A3 status {a3['status']} != expected {exp['A3_status']}")

    identity = expected["identity_assertion_id"]
    for assertion in view["assertions"]:
        if assertion["id"] == identity:
            if assertion["status"] != "current":
                failures.append(f"Identity assertion not current")
            if assertion["value"] != "Jordan Ellis":
                failures.append("Identity value changed")

    active_income = exp["active_income_assertion_id"]
    income_row = next((a for a in view["assertions"] if a["id"] == active_income), None)
    if not income_row or income_row["status"] != "current":
        failures.append("September income assertion should be current after correction")

    aug = next((a for a in view["assertions"] if a["id"] == "assert_income_aug"), None)
    if aug and aug["status"] != "superseded":
        failures.append("August income assertion should be superseded after correction")

    affected = {a["id"] for a in view["assessments"] if a["status"] in ("current", "stale") and a["id"] in exp["affected_assessment_ids"]}
    if not {"A1", "A2"}.issubset({x["id"] for x in view["assessments"]}):
        failures.append("Missing assessments")

    if view["ready_to_export"] != exp["ready_to_export"]:
        failures.append(
            f"ready_to_export {view['ready_to_export']} != expected {exp['ready_to_export']}"
        )

    if set(view["conflicts"]) != set(exp["unresolved_conflicts"]):
        failures.append(f"conflicts {view['conflicts']} != {exp['unresolved_conflicts']}")

    if failures:
        print("CHECK FAILED:")
        for f in failures:
            print(" -", f)
        return 1

    print("CHECK PASSED: case matches expected.json after correction workflow")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

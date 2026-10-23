#!/usr/bin/env python3
"""Smoke test MCP tools in-process (Streamable HTTP optional)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from server.ledger import CaseStore
from server.paths import DEFAULT_DB

# In-process tool calls mirror mcp_server.py
import mcp_server as mcp_mod


def main() -> int:
    db = DEFAULT_DB
    if db.exists():
        db.unlink()
    mcp_mod._store_instance = None

    state = json.loads(mcp_mod.get_case())
    assert state["case_revision"] == 0

    prop = json.loads(mcp_mod.propose_correction("adviser"))
    if "error" in prop:
        print("FAIL propose:", prop)
        return 1

    result = json.loads(
        mcp_mod.confirm_correction(prop["proposal_id"], "applicant")
    )
    if "error" in result:
        print("FAIL confirm:", result)
        return 1

    packet = json.loads(mcp_mod.export_handoff_packet())
    if packet["case_revision"] < 1:
        print("FAIL receipt revision")
        return 1

    print("MCP SMOKE PASSED (in-process tools)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

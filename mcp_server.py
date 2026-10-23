"""MCP Streamable HTTP server exposing Handover ledger tools."""

from __future__ import annotations

import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from server.ledger import CaseStore, LedgerError
from server.paths import DEFAULT_DB

mcp = FastMCP("Handover", json_response=True)
_store_instance: CaseStore | None = None


def get_store() -> CaseStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = CaseStore(DEFAULT_DB)
        _store_instance.init_schema()
        row = _store_instance.conn.execute("SELECT COUNT(*) AS c FROM documents").fetchone()
        if row["c"] == 0:
            _store_instance.reset_from_fixture()
    return _store_instance


@mcp.tool()
def get_case() -> str:
    """Return current case state including revision, assessments, and ledger tail."""
    return json.dumps(get_store().get_case_view(), indent=2)


@mcp.tool()
def inspect_source(assessment_id: str = "A1") -> str:
    """Show supporting assertions and document hashes for an assessment."""
    return json.dumps(get_store().inspect_source(assessment_id), indent=2)


@mcp.tool()
def propose_correction(actor_role: str = "adviser") -> str:
    """Propose swapping August payslip income evidence for September."""
    try:
        return json.dumps(get_store().propose_income_correction(actor_role), indent=2)
    except LedgerError as e:
        return json.dumps({"error": e.code, "message": e.message})


@mcp.tool()
def confirm_correction(proposal_id: str, actor_role: str = "applicant") -> str:
    """Applicant confirms a pending correction proposal."""
    try:
        return json.dumps(get_store().confirm_proposal(proposal_id, actor_role), indent=2)
    except LedgerError as e:
        return json.dumps({"error": e.code, "message": e.message})


@mcp.tool()
def export_handoff_packet() -> str:
    """Export JSON handoff receipt with provenance and conflicts."""
    return json.dumps(get_store().export_receipt(), indent=2)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")

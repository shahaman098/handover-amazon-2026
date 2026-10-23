"""Bounded intent handling — no LLM required."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from server.ledger import CaseStore, LedgerError


PAYSLIP_RE = re.compile(
    r"(old\s+payslip|payslip).*(september|sep)|september.*(payslip|document)",
    re.I,
)
INSPECT_RE = re.compile(r"inspect|show\s+source|where\s+did", re.I)
CLARIFY_SEP = re.compile(r"september|sep", re.I)
CLARIFY_AUG = re.compile(r"august|aug", re.I)


def handle_intent(
    store: CaseStore,
    role: str,
    text: str,
    clarify_choice: Optional[str] = None,
) -> Dict[str, Any]:
    text = text.strip()
    if not text:
        return {"kind": "message", "message": "Say what you want to review or correct."}

    if INSPECT_RE.search(text) or text.lower().startswith("source for"):
        info = store.inspect_source("A1")
        src = info["sources"][0] if info["sources"] else {}
        return {
            "kind": "message",
            "message": (
                f"Assessment A1 ({info['assessment_title']}) currently shows "
                f"{info['current_value']}. Source: {src.get('document_title')} "
                f"(assertion {src.get('assertion_id')}, hash {src.get('content_hash')})."
            ),
        }

    if PAYSLIP_RE.search(text) or (
        clarify_choice and clarify_choice in ("doc_payslip_sep", "september")
    ):
        if clarify_choice in (None, "") and "september" not in text.lower() and "sep" not in text.lower():
            return {
                "kind": "clarify",
                "message": "Which payslip should replace the old one?",
                "options": [
                    {"id": "doc_payslip_sep", "label": "Payslip September 2026"},
                    {"id": "doc_payslip_aug", "label": "Payslip August 2026 (older)"},
                ],
            }
        if clarify_choice == "doc_payslip_aug" or CLARIFY_AUG.search(text):
            return {
                "kind": "message",
                "message": "August is the document being replaced. Choose September instead.",
            }
        try:
            prop = store.propose_income_correction(role, to_document_id="doc_payslip_sep")
        except LedgerError as e:
            return {"kind": "message", "message": e.message}
        return {
            "kind": "proposal",
            "message": (
                "Proposed correction: swap income evidence from August payslip to "
                f"September (£{prop['new_income_value']}). Affected assessments: "
                f"{', '.join(prop['affected_assessment_ids'])}. Applicant must confirm."
            ),
            "proposal_id": prop["proposal_id"],
            "proposal": prop,
        }

    if clarify_choice and clarify_choice == "doc_payslip_sep":
        try:
            prop = store.propose_income_correction(role, to_document_id="doc_payslip_sep")
        except LedgerError as e:
            return {"kind": "message", "message": e.message}
        return {
            "kind": "proposal",
            "message": "September payslip selected. Review and confirm.",
            "proposal_id": prop["proposal_id"],
            "proposal": prop,
        }

    return {
        "kind": "message",
        "message": (
            "I can inspect income sources or help correct payslip evidence. "
            "Try: 'That is my old payslip. Use the September document instead.'"
        ),
    }


def extract_custom_income(text: str) -> Optional[str]:
    m = re.search(r"\b(\d{4,5})\b", text)
    return m.group(1) if m else None

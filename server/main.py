"""FastAPI application for Handover."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from server.conversation import extract_custom_income, handle_intent
from server.ledger import CaseStore, LedgerError
from server.models import ConfirmRequest, IntentRequest, ProposalCreateRequest
from server.paths import DEFAULT_DB

store = CaseStore(DEFAULT_DB)
store.init_schema()
_row = store.conn.execute("SELECT COUNT(*) AS c FROM documents").fetchone()
if _row["c"] == 0:
    store.reset_from_fixture()

app = FastAPI(title="Handover", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _err(exc: LedgerError) -> HTTPException:
    status = 409 if exc.code == "stale_revision" else 400
    if exc.code == "not_found":
        status = 404
    if exc.code == "forbidden":
        status = 403
    return HTTPException(status_code=status, detail={"code": exc.code, "message": exc.message})


@app.get("/api/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/api/case")
def get_case() -> Dict[str, Any]:
    return store.get_case_view()


@app.post("/api/reset")
def reset_case() -> Dict[str, Any]:
    store.reset_from_fixture()
    return {"ok": True, "case_revision": store.get_case_view()["case_revision"]}


@app.post("/api/intent")
def post_intent(body: IntentRequest, clarify_choice: Optional[str] = None) -> Dict[str, Any]:
    return handle_intent(store, body.role, body.text, clarify_choice=clarify_choice)


@app.post("/api/intent/clarify")
def post_intent_clarify(body: IntentRequest, choice: str) -> Dict[str, Any]:
    return handle_intent(store, body.role, body.text, clarify_choice=choice)


@app.post("/api/proposals/{proposal_id}/confirm")
def confirm_proposal(proposal_id: str, body: ConfirmRequest) -> Dict[str, Any]:
    try:
        return store.confirm_proposal(proposal_id, body.role)
    except LedgerError as e:
        raise _err(e) from e


@app.post("/api/proposals/{proposal_id}/cancel")
def cancel_proposal(proposal_id: str) -> Dict[str, str]:
    store.cancel_proposal(proposal_id)
    return {"ok": "cancelled"}


@app.post("/api/proposals")
def create_proposal(
    body: ProposalCreateRequest,
    if_match_revision: Optional[int] = Header(None, alias="If-Match-Revision"),
) -> Dict[str, Any]:
    rev = if_match_revision if if_match_revision is not None else body.case_revision
    try:
        return store.propose_income_correction(
            body.role,
            expected_revision=rev,
        )
    except LedgerError as e:
        raise _err(e) from e


@app.get("/api/inspect/{assessment_id}")
def inspect(assessment_id: str) -> Dict[str, Any]:
    return store.inspect_source(assessment_id)


@app.get("/api/receipt")
def receipt() -> Dict[str, Any]:
    return store.export_receipt()


@app.post("/api/proposals/custom-income")
def propose_custom_income(body: IntentRequest) -> Dict[str, Any]:
    val = extract_custom_income(body.text)
    if not val:
        raise HTTPException(400, "Include a numeric income in the message")
    try:
        return store.propose_income_correction(body.role, custom_income=val)
    except LedgerError as e:
        raise _err(e) from e


@app.get("/api/check/cycle")
def check_cycle() -> Dict[str, Any]:
    ok, msg = store.try_cycle_edge()
    return {"would_cycle": not ok, "message": msg}


@app.exception_handler(LedgerError)
def ledger_handler(_request, exc: LedgerError):
    return JSONResponse(
        status_code=409 if exc.code == "stale_revision" else 400,
        content={"code": exc.code, "message": exc.message},
    )

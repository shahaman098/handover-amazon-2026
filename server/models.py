from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

Role = Literal["applicant", "adviser"]


class IntentRequest(BaseModel):
    role: Role
    text: str


class ClarifyOption(BaseModel):
    id: str
    label: str


class IntentResponse(BaseModel):
    kind: Literal["message", "clarify", "proposal"]
    message: str
    options: List[ClarifyOption] = Field(default_factory=list)
    proposal_id: Optional[str] = None
    proposal: Optional[Dict[str, Any]] = None


class ConfirmRequest(BaseModel):
    role: Role = "applicant"


class ProposalCreateRequest(BaseModel):
    role: Role
    from_assertion_id: str
    to_assertion_id: str
    case_revision: int


class DocumentView(BaseModel):
    id: str
    title: str
    version: int
    role: Optional[str] = None
    content_preview: str


class AssertionView(BaseModel):
    id: str
    key: str
    value: str
    document_id: str
    status: str
    coverage: str
    superseded_by: Optional[str] = None


class AssessmentView(BaseModel):
    id: str
    title: str
    status: str
    value: Optional[str] = None
    explanation: Optional[str] = None
    depends_on: List[str]


class CaseView(BaseModel):
    case_id: str
    title: str
    case_revision: int
    documents: List[DocumentView]
    assertions: List[AssertionView]
    assessments: List[AssessmentView]
    checklist: List[Dict[str, Any]]
    conflicts: List[str]
    ready_to_export: bool
    active_proposal_id: Optional[str] = None
    ledger_tail: List[Dict[str, Any]]

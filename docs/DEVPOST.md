# Devpost submission draft (entrant submits)

## Project name

Handover

## Tagline

Keep application draft answers consistent when evidence changes — with a provenance ledger you can hand off.

## Track

**Alexa+** — entrant-built conversational simulation (web client + local API). MCP tools included (`mcp` SDK 1.x Streamable HTTP server).

## Description (English)

Community advisers and applicants often exchange revised documents while preparing support applications. When one document is wrong or outdated, several draft answers can become stale — but a chat message alone does not record which answers were reviewed or which evidence version the next adviser should trust.

**Handover** is a voice-style conversational workspace (web simulation) backed by a server-enforced provenance ledger:

- Inspect which document supports each draft answer
- Propose a correction with explicit affected assessments
- Require **applicant confirmation** bound to case revision and proposal hash
- Atomically supersede evidence, recompute dependents, and append an audit event
- Reject stale or duplicate confirmations without partial writes
- Export a handoff receipt with unresolved conflicts and unknown coverage flagged

All data is **fictional** (Riverside Support Program fixture). Dependency edges are **authored** in an inspectable manifest — not inferred from arbitrary PDFs. Applicant and adviser roles are **simulated**.

## Video

*(Add public YouTube/Vimeo URL after recording — target under 3 minutes.)*

## Repository

*(Add private GitHub URL — grant Devpost reviewers access.)*

## Tool feedback

See [TOOL_FEEDBACK.md](TOOL_FEEDBACK.md) in the repository.

## Built during hackathon

Yes — new repository created 23 October 2026 for this event.

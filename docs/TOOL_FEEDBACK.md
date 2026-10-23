# Developer tool feedback (Devpost)

## Cursor

- **Purpose:** IDE pair-programming for server, scripts, and React UI in one day.
- **Strengths:** Fast iteration across Python and TypeScript; integrated terminal.
- **Shortcomings:** Large multi-file plans need careful scope control to avoid drift.
- **Onboarding:** Familiar VS Code-style layout.
- **Use again:** Yes — for time-boxed full-stack spikes.

## Python 3.12

- **Purpose:** Ledger, API, verification scripts.
- **Strengths:** Stable typing and SQLite in stdlib.
- **Shortcomings:** Environment must be pinned (avoid 3.14 for some wheels during hackathon).
- **Use again:** Yes.

## FastAPI + Uvicorn

- **Purpose:** REST API for simulation client and tests.
- **Strengths:** Quick routing, JSON models, clear errors for stale revision.
- **Shortcomings:** Single-process store; production would need injected session per request at scale.
- **Use again:** Yes for demos and internal tools.

## SQLite (WAL)

- **Purpose:** Transactional persistence and append-only event log.
- **Strengths:** Atomic commits, easy reset for judges.
- **Shortcomings:** Not multi-tenant without migration design.
- **Use again:** Yes for local provenance prototypes.

## MCP Python SDK (1.x, FastMCP)

- **Purpose:** Expose ledger tools for Alexa+ MCP path.
- **Strengths:** Thin wrapper over domain logic.
- **Shortcomings:** 2.x breaking rename required pinning `<2`; Streamable HTTP setup docs still evolving.
- **Use again:** Yes after checking migration guide for 2.x.

## Vite + React

- **Purpose:** Alexa-style chat UI and confirmation card.
- **Strengths:** Fast dev server, proxy to API.
- **Shortcomings:** Not a voice shell — simulation is intentional.
- **Use again:** Yes.

## npm

- **Purpose:** Frontend dependencies.
- **Strengths:** Standard toolchain.
- **Shortcomings:** Extra install step for judges.
- **Use again:** Yes.

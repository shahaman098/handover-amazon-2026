# Handover

**Alexa+ track (entrant-built simulation)** for the [Build, Ship, Shape: Amazon Developer Hackathon](https://amazonappdev2026.devpost.com/).

Handover keeps fictional application draft answers aligned when supporting documents change. A server-enforced provenance ledger records confirmations, supersedes evidence, invalidates dependent answers, and rejects stale writes.

> This is **not** a production Alexa+ device or Amazon partner console integration. Roles (applicant / adviser) are simulated.

## Private repository access

This repo is **private**. Judges: request access via the Devpost submission or contact the entrant. You need:

- Python 3.12+
- Node.js 18+ (for the web UI)

## Quick start

```bash
cd handover
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Reset fictional Riverside case
PYTHONPATH=. python scripts/reset_db.py

# API (port 8020)
PYTHONPATH=. uvicorn server.main:app --host 127.0.0.1 --port 8020

# Web UI (port 5173) — separate terminal
cd web && npm install && npm run dev
```

Open http://localhost:5173

## Verification

```bash
PYTHONPATH=. python scripts/run_verification.py
PYTHONPATH=. python scripts/check_case.py
PYTHONPATH=. python scripts/mcp_smoke.py
```

## MCP (optional Streamable HTTP)

MCP tools mirror the ledger (`get_case`, `inspect_source`, `propose_correction`, `confirm_correction`, `export_handoff_packet`). Uses `mcp` SDK **1.x** (pinned `<2`).

```bash
PYTHONPATH=. python mcp_server.py
```

See [docs/RUNTIME.md](docs/RUNTIME.md).

## Demo script

See [docs/DEMO.md](docs/DEMO.md).

## License

MIT — see [LICENSE](LICENSE).

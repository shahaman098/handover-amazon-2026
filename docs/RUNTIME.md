# Runtime decisions

## Alexa+ simulation route

The web client is an entrant-built conversational simulation. It calls the local REST API; no speech SDK or physical device is required.

## MCP hour-1 gate

- **Result:** PASSED (in-process tool smoke via `scripts/mcp_smoke.py`).
- **Package:** `mcp>=1.9,<2` (FastMCP). MCP 2.x renamed APIs; we pin v1 for Streamable HTTP compatibility during the hackathon window.
- **Transport:** Run `python mcp_server.py` for a separate Streamable HTTP MCP server. Tools call the same `CaseStore` as the REST API.
- **Fallback:** If MCP HTTP is unavailable in a judge environment, the REST + web simulation fully demonstrates the ledger (per Devpost Alexa+ FAQ).

## Bounded conversation

Utterances are matched with regex / keywords in `server/conversation.py`. Unsupported text receives a help message — no LLM API is required for the demo.

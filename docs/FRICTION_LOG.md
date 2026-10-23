# Friction log (observed today)

1. **MCP SDK 2.x install** — Default `mcp` resolved to 2.x where `FastMCP` moved to `MCPServer`. **Repro:** `pip install mcp` on clean venv; import `mcp.server.fastmcp` fails. **Workaround:** Pin `mcp>=1.9,<2` in `requirements.txt`.

2. **MCP module naming** — Global `_store` variable shadowed `get_store()` helper when tool function named `get_case`. **Workaround:** Rename to `_store_instance` / `get_store()`.

"""
Grants.gov MCP Server

Provides tools to search federal grant opportunities via the Grants.gov API.
No authentication is required to use this server.
"""

import os

from fastmcp import FastMCP

from grants_gov_mcp.prompts import register_prompts
from grants_gov_mcp.routes import register_routes
from grants_gov_mcp.tools import register_tools

mcp = FastMCP("grants_gov_mcp")

register_routes(mcp)
register_tools(mcp)
register_prompts(mcp)

if __name__ == "__main__":
    # Transport selection:
    # - If a platform port env var is set (PORT / DATABRICKS_APP_PORT), serve MCP
    #   over streamable HTTP on that port at the fixed path /mcp, with a /health
    #   readiness endpoint. This is the mode the container image uses so the Obot
    #   MCP gateway can host it as a `containerized` server (`:8080/mcp`, health
    #   at `/health`) — the Dockerfile sets PORT=8080.
    # - Otherwise fall back to stdio for local MCP clients (Claude Desktop, etc.).
    #
    # Note on authentication: the server intentionally sets no FastMCP `auth`
    # provider. In the gateway-hosted `containerized` model the container has no
    # public route — the Obot gateway is the only caller and it enforces access
    # (transport auth). 
    port_env = os.getenv("DATABRICKS_APP_PORT") or os.getenv("PORT")
    if port_env:
        mcp.run(transport="http", host="0.0.0.0", port=int(port_env), path="/mcp")
    else:
        mcp.run(transport="stdio")

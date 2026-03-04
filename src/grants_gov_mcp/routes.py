from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse


def register_routes(mcp: FastMCP) -> None:
    """Register custom HTTP routes on the MCP server."""

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "ok", "server": "grants_gov_mcp"})

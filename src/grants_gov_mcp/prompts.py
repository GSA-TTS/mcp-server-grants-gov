from fastmcp import FastMCP


def register_prompts(mcp: FastMCP) -> None:
    """Register MCP prompts for the grants.gov server."""

    @mcp.prompt()
    def search_grants_help() -> str:
        """Explain how to search for grant opportunities on Grants.gov."""
        return (
            "You can search for federal grant opportunities using the `grants_gov_search_opportunities` tool.\n\n"
            "**Common search patterns:**\n"
            "- Keyword search: Set `keyword` to find grants matching a topic (e.g., 'climate', 'maternal health')\n"
            "- Filter by status: Set `opp_statuses` to ['posted'] for currently open grants\n"
            "- Filter by agency: Set `agencies` to agency codes like ['HHS', 'NSF', 'DOE']\n"
            "- Filter by eligibility: Set `eligibilities` to eligibility codes\n"
            "- Filter by category: Set `funding_categories` to category codes like ['HL', 'ED']\n"
            "- Look up a specific grant: Set `opp_num` to the exact opportunity number\n\n"
            "**Pagination:** Use `rows` (1–100) and `start_record` (1-indexed) to page through results.\n\n"
            "**Output formats:** Set `response_format` to 'markdown' (default) or 'json'."
        )

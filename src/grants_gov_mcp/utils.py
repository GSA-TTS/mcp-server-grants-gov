import json
from typing import Any

import httpx

SEARCH2_URL = "https://api.grants.gov/v1/api/search2"
REQUEST_TIMEOUT = 30.0


async def make_search2_request(payload: dict[str, Any]) -> dict[str, Any]:
    """POST the payload to the grants.gov search2 endpoint and return parsed JSON."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            SEARCH2_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()


def handle_api_error(e: Exception) -> str:
    """Return a clear, actionable error message for common HTTP and network failures."""
    if isinstance(e, httpx.HTTPStatusError):
        status = e.response.status_code
        if status == 400:
            return (
                "Error: Bad request — one or more parameters are invalid. "
                "Check that agency codes, eligibility codes, and funding category codes are correct."
            )
        if status == 429:
            return "Error: Rate limit exceeded. Please wait before retrying."
        if status >= 500:
            return f"Error: Grants.gov server error ({status}). The API may be temporarily unavailable."
        return f"Error: API request failed with status {status}."
    if isinstance(e, httpx.TimeoutException):
        return "Error: Request timed out. The Grants.gov API may be slow — try again or reduce the number of rows."
    if isinstance(e, httpx.ConnectError):
        return "Error: Could not connect to Grants.gov. Check your internet connection."
    return f"Error: Unexpected error — {type(e).__name__}: {e}"


def _format_date(date_str: str | None) -> str:
    """Return date string as-is or 'N/A' if missing."""
    return date_str if date_str else "N/A"


def format_opportunity_markdown(opp: dict[str, Any]) -> str:
    """Format a single opportunity dict into a Markdown block."""
    title = opp.get("title", "Untitled")
    number = opp.get("number", "N/A")
    agency = opp.get("agencyName", opp.get("agencyCode", "N/A"))
    status = opp.get("oppStatus", "N/A")
    open_date = _format_date(opp.get("openDate"))
    close_date = _format_date(opp.get("closeDate"))
    doc_type = opp.get("docType", "N/A")
    aln_list = opp.get("alnlist", "")

    lines = [
        f"### {title}",
        f"- **Opportunity #**: {number}",
        f"- **Agency**: {agency}",
        f"- **Status**: {status}",
        f"- **Open Date**: {open_date}",
        f"- **Close Date**: {close_date}",
        f"- **Type**: {doc_type}",
    ]
    if aln_list:
        lines.append(f"- **ALN**: {aln_list}")
    return "\n".join(lines)


def format_search_results_markdown(
    data: dict[str, Any],
    rows: int,
    start_record: int,
) -> str:
    """Format the full search2 response data as Markdown."""
    hit_count: int = data.get("hitCount", 0)
    opp_hits: list[dict] = data.get("oppHits", [])

    if not opp_hits:
        return "No grant opportunities found matching your search criteria."

    shown = len(opp_hits)
    end_record = start_record + shown - 1
    has_more = hit_count > end_record

    lines = [
        f"## Grants.gov Search Results",
        f"",
        f"**Total matches**: {hit_count:,}  |  "
        f"**Showing**: {start_record}–{end_record}",
        f"",
    ]

    for opp in opp_hits:
        lines.append(format_opportunity_markdown(opp))
        lines.append("")

    if has_more:
        next_start = end_record + 1
        lines.append(
            f"---\n*{hit_count - end_record:,} more results available. "
            f"Use `start_record={next_start}` and `rows={rows}` to fetch the next page.*"
        )

    return "\n".join(lines)


def build_search_payload(
    keyword: str | None,
    opp_num: str | None,
    agencies: list[str] | None,
    opp_statuses: list[str] | None,
    eligibilities: list[str] | None,
    funding_categories: list[str] | None,
    aln: str | None,
    rows: int,
    start_record: int,
) -> dict[str, Any]:
    """Build the JSON payload for a search2 POST request."""
    payload: dict[str, Any] = {
        "rows": rows,
        "startRecord": start_record,
    }
    if keyword:
        payload["keyword"] = keyword
    if opp_num:
        payload["oppNum"] = opp_num
    if agencies:
        payload["agencies"] = "|".join(agencies)
    if opp_statuses:
        payload["oppStatuses"] = "|".join(opp_statuses)
    if eligibilities:
        payload["eligibilities"] = "|".join(eligibilities)
    if funding_categories:
        payload["fundingCategories"] = "|".join(funding_categories)
    if aln:
        payload["aln"] = aln
    return payload

#!/usr/bin/env python3
"""EstWarden MCP Server — Model Context Protocol for LLM tool use.

Any MCP-compatible LLM (Claude, GPT, etc.) can query Baltic threat intelligence.

Tools:
  get_threat_level    — current threat level + score
  get_report          — daily report with indicators
  get_signals         — recent signals by source
  get_narratives      — active narrative classifications
  get_campaigns       — detected influence campaigns
  search_signals      — full-text search across signals

Usage:
  python3 server.py                           # stdio transport
  python3 server.py --transport sse --port 8080  # SSE transport

Requires: pip install mcp
"""

import json
import urllib.request
from datetime import datetime

API_BASE = "https://estwarden.eu"

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("Install MCP: pip install mcp")
    exit(1)

server = Server("estwarden")


def api_get(path):
    """Fetch from EstWarden public API."""
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "EstWarden-MCP/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_threat_level",
            description="Get the current Baltic threat level (GREEN/YELLOW/ORANGE/RED) and Composite Threat Index score (0-100).",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_report",
            description="Get the daily intelligence report with threat indicators for a specific date.",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD format (default: today)"}
                },
            },
        ),
        Tool(
            name="get_narratives",
            description="Get active disinformation narrative classifications (N1-N5) targeting Baltic states.",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "description": "Lookback period in days (default: 7)"}
                },
            },
        ),
        Tool(
            name="get_campaigns",
            description="Get detected coordinated influence campaigns targeting the Baltic region.",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "description": "Lookback period in days (default: 30)"}
                },
            },
        ),
        Tool(
            name="get_history",
            description="Get threat level history over time for trend analysis.",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "description": "Number of days (default: 30, max: 365)"}
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name, arguments):
    try:
        if name == "get_threat_level":
            data = api_get("/api/threat-index")
            return [TextContent(
                type="text",
                text=f"Baltic Threat Level: {data.get('level', 'UNKNOWN')}\n"
                     f"Composite Threat Index: {data.get('score', 0):.1f}/100\n"
                     f"Date: {data.get('date', 'unknown')}\n"
                     f"Sources: {data.get('source_count', 'unknown')} active collectors"
            )]

        elif name == "get_report":
            date = arguments.get("date", datetime.now().strftime("%Y-%m-%d"))
            data = api_get(f"/api/report/{date}")
            indicators = data.get("indicators", [])
            ind_text = "\n".join(
                f"  [{i['status']}] {i['category']}/{i['label']}: {i['finding']}"
                for i in indicators
            )
            return [TextContent(
                type="text",
                text=f"Intelligence Report — {date}\n"
                     f"Threat Level: {data.get('threat_level', '?')}\n"
                     f"Summary: {data.get('summary', 'No summary')}\n\n"
                     f"Indicators:\n{ind_text or '  (none)'}"
            )]

        elif name == "get_narratives":
            days = arguments.get("days", 7)
            data = api_get(f"/api/influence/narratives?days={days}")
            items = data if isinstance(data, list) else data.get("narratives", [])
            text = "Active Narrative Classifications (Baltic region):\n\n"
            codes = {
                "N1": "Russophobia/Persecution", "N2": "War Escalation Panic",
                "N3": "Aid = Theft", "N4": "Delegitimization", "N5": "Isolation/Victimhood"
            }
            for item in items:
                code = item.get("code", "?")
                text += f"  {code} ({codes.get(code, '?')}): {item.get('count', 0)} signals\n"
            return [TextContent(type="text", text=text)]

        elif name == "get_campaigns":
            days = arguments.get("days", 30)
            data = api_get(f"/api/influence/campaigns?days={days}")
            items = data if isinstance(data, list) else data.get("campaigns", [])
            text = f"Detected Influence Campaigns (last {days} days):\n\n"
            for c in items:
                text += f"  • {c.get('name', '?')} [{c.get('severity', '?')}]\n"
                text += f"    {c.get('summary', 'No summary')[:200]}\n\n"
            if not items:
                text += "  (none detected)\n"
            return [TextContent(type="text", text=text)]

        elif name == "get_history":
            days = arguments.get("days", 30)
            data = api_get(f"/api/history?days={days}")
            items = data if isinstance(data, list) else data.get("history", [])
            text = f"Threat Level History (last {days} days):\n\n"
            for entry in items[-14:]:  # Last 14 entries
                text += f"  {entry.get('date', '?')}: {entry.get('level', '?')} ({entry.get('score', 0):.0f}/100)\n"
            return [TextContent(type="text", text=text)]

        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]


async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", default="stdio", choices=["stdio", "sse"])
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    if args.transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        import uvicorn
        sse = SseServerTransport("/messages")
        app = Starlette(routes=[
            sse.get_sse_route("/sse", server),
            sse.get_message_route("/messages", server),
        ])
        uvicorn.run(app, host="0.0.0.0", port=args.port)
    else:
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

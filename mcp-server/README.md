# EstWarden MCP Server

[Model Context Protocol](https://modelcontextprotocol.io/) server that gives any LLM access to Baltic threat intelligence.

## Tools

| Tool | What it returns |
|------|----------------|
| `get_threat_level` | Current threat level (GREEN/YELLOW/ORANGE/RED) + CTI score |
| `get_report` | Daily intelligence report with indicators |
| `get_narratives` | Active disinformation narrative classifications (N1-N5) |
| `get_campaigns` | Detected influence campaigns |
| `get_history` | Threat level trends over time |

## Setup

```bash
pip install mcp
python3 server.py
```

### Claude Desktop

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "estwarden": {
      "command": "python3",
      "args": ["/path/to/server.py"]
    }
  }
}
```

### SSE Transport (for remote access)

```bash
pip install mcp uvicorn starlette
python3 server.py --transport sse --port 8080
```

## Example

Ask Claude: *"What's the current Baltic threat level and are there any active influence campaigns?"*

Claude will call `get_threat_level` and `get_campaigns` and synthesize a response.

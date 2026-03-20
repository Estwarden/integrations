# EstWarden Integrations

Community integration examples for [EstWarden](https://estwarden.eu) — the Baltic Security Intelligence platform. Connect threat data to your tools, dashboards, assistants, and automations.

## Integrations

| Integration | What it does | Status |
|---|---|---|
| [**OpenClaw Skill**](openclaw-skill/) | AI assistant skill — threat level, reports, narratives, campaigns | ✅ Ready |
| [**MCP Server**](mcp-server/) | Model Context Protocol — any LLM queries threat data | ✅ Ready |
| [**Grafana Dashboards**](grafana/) | Threat overview + collector health dashboards | ✅ Ready |
| [**Home Assistant**](home-assistant/) | Smart home sensors, automations on threat changes | ✅ Ready |
| [**Telegram Bot**](telegram-bot/) | Query threats from Telegram (/threat, /report, /narr) | ✅ Ready |
| [**CLI**](cli/) | Terminal threat queries — `estwarden threat` | ✅ Ready |
| [**n8n Workflows**](n8n-workflows/) | Slack briefing, email alerts, visual automation | ✅ Ready |
| [**Obsidian Plugin**](obsidian-plugin/) | Daily threat notes in your vault | 💡 Concept |
| [**Examples**](examples/) | Python, Go, JavaScript code snippets | ✅ Ready |

## Public API

All integrations use the public API. No key required.

```
GET https://estwarden.eu/api/threat-index       — CTI score + level
GET https://estwarden.eu/api/today              — daily report
GET https://estwarden.eu/api/report/{date}      — historical report
GET https://estwarden.eu/api/history?days=30    — threat trend
GET https://estwarden.eu/api/influence/narratives — narrative activity
GET https://estwarden.eu/api/influence/campaigns  — influence campaigns
GET https://estwarden.eu/api/trends             — trend analysis
GET https://estwarden.eu/feed.xml               — RSS feed
GET https://estwarden.eu/health                 — service health
```

## Contributing

Add your integration — fork, create a directory, submit a PR.

## License

MIT

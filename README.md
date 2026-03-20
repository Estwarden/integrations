# EstWarden Integrations

Community integration examples for [EstWarden](https://estwarden.eu) — the Baltic Security Intelligence platform. Use these to connect EstWarden data to your tools, dashboards, assistants, and automations.

## Integrations

| Integration | What it does | Status |
|---|---|---|
| [**MCP Server**](mcp-server/) | Model Context Protocol server — any LLM can query threat data, signals, narratives | ✅ Ready |
| [**Grafana Dashboards**](grafana/) | Pre-built dashboards for collector health, signal flow, threat index | ✅ Ready |
| [**Home Assistant**](home-assistant/) | Threat level sensor, Baltic security card, automations on threat changes | ✅ Ready |
| [**Telegram Bot**](telegram-bot/) | Query threat level, subscribe to alerts, get daily briefings | 📦 Example |
| [**n8n Workflows**](n8n-workflows/) | Visual automation — connect EstWarden to Slack, Email, Notion, etc. | 📦 Example |
| [**CLI Tool**](cli/) | Command-line interface for querying EstWarden public API | 📦 Example |
| [**Obsidian Plugin**](obsidian-plugin/) | Daily threat notes in your Obsidian vault | 💡 Concept |
| [**Examples**](examples/) | Code snippets for Python, Go, JavaScript, curl | ✅ Ready |

## Public API

All integrations use the EstWarden public API:

```
GET https://estwarden.eu/api/today          — today's threat report
GET https://estwarden.eu/api/threat-index   — current CTI score + level
GET https://estwarden.eu/api/history?days=30 — threat level history
GET https://estwarden.eu/api/influence/latest — influence ecosystem
GET https://estwarden.eu/api/influence/narratives — narrative activity
GET https://estwarden.eu/api/influence/campaigns — active campaigns
GET https://estwarden.eu/api/trends         — trend analysis
GET https://estwarden.eu/api/space-weather  — space weather data
GET https://estwarden.eu/api/ioda           — internet outage data
GET https://estwarden.eu/health             — service health
GET https://estwarden.eu/feed.xml           — RSS feed
```

No API key required. No rate limiting (be reasonable). JSON responses.

## Contributing

Add your integration! Fork, create a directory, add a README with setup instructions, submit a PR.

## License

MIT — all integrations are independently licensed by their authors.

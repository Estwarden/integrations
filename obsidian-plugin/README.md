# EstWarden Obsidian Plugin (Concept)

Daily Baltic threat intelligence notes in your Obsidian vault.

## Concept

A community plugin that:
1. Fetches today's report from `https://estwarden.eu/api/today`
2. Creates a daily note in `EstWarden/YYYY-MM-DD.md`
3. Includes threat level, indicators, narrative activity
4. Links to related notes (campaigns, persons, locations)

## Note Template

```markdown
---
date: {{date}}
threat_level: {{level}}
cti_score: {{score}}
tags: [estwarden, baltic-security]
---

# 🛡 Baltic Security — {{date}}

**Threat Level:** {{level}} ({{score}}/100)

## Summary
{{summary}}

## Indicators
{{#indicators}}
- [{{status}}] **{{category}}/{{label}}**: {{finding}}
{{/indicators}}

## Active Campaigns
{{#campaigns}}
- [[Campaign — {{name}}]]: {{summary}}
{{/campaigns}}

---
*Source: [estwarden.eu](https://estwarden.eu)*
```

## Implementation Status

💡 **Concept** — looking for a contributor to build this as an Obsidian community plugin.

The API is simple (public JSON, no auth). The main work is:
- Obsidian plugin boilerplate (TypeScript)
- Settings UI (vault path, update interval)
- Note templating with Mustache/Handlebars
- Optional: backfill historical notes

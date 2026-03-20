---
name: estwarden
description: >
  Query Baltic security intelligence from EstWarden. Get threat levels,
  daily reports, narrative classifications, influence campaigns, and trend
  analysis. Uses the public API at estwarden.eu — no API key required.
---

# EstWarden Skill

Query Baltic security threat data from the EstWarden public API.

## Tools

All commands use `scripts/estwarden-query.sh` in this skill directory.

### Threat Level
```bash
./scripts/estwarden-query.sh threat
```
Returns: current threat level (GREEN/YELLOW/ORANGE/RED) and CTI score (0-100).

### Daily Report
```bash
./scripts/estwarden-query.sh report [date]
```
Returns: intelligence summary with threat indicators for today or a specific date.

### Narrative Activity
```bash
./scripts/estwarden-query.sh narratives [days]
```
Returns: active disinformation narrative classifications (N1-N5) targeting Baltic states.

### Influence Campaigns
```bash
./scripts/estwarden-query.sh campaigns [days]
```
Returns: detected coordinated influence campaigns.

### Threat History
```bash
./scripts/estwarden-query.sh history [days]
```
Returns: threat level trend over time.

### Signal Freshness
```bash
./scripts/estwarden-query.sh health
```
Returns: API health status.

## When to use

Use this skill when the user asks about:
- Baltic security, Estonian security, threat level
- Russian military activity near Baltic states
- Disinformation, influence operations, narratives
- NATO/Baltic defense situation
- Threat trends, daily briefing

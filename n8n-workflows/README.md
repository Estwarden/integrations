# EstWarden n8n Workflows

Visual automation workflows for connecting EstWarden data to other tools.

## Workflows

### 1. Daily Slack Briefing
Poll `/api/today` every morning → format as Slack message → post to #security channel.

### 2. Threat Level → Email Alert  
Watch `/api/threat-index` every 15 min → if level changes → send email to distribution list.

### 3. New Campaign → Notion Database
Poll `/api/influence/campaigns` → on new campaign → create Notion page with details.

### 4. RSS → Discord
Watch `/feed.xml` → on new entry → post to Discord webhook with embed.

### 5. Weekly PDF Report
Every Monday → fetch 7-day history → generate PDF → email to stakeholders.

## Setup

1. Import the workflow JSON into your n8n instance
2. Configure credentials (Slack token, email, etc.)
3. Activate the workflow

## Trigger Node

Use the **HTTP Request** node with:
```
URL: https://estwarden.eu/api/threat-index
Method: GET
Response Format: JSON
```

No authentication needed for public API endpoints.

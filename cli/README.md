# EstWarden CLI

Query Baltic threat intelligence from your terminal.

## Install

```bash
curl -sL https://raw.githubusercontent.com/Estwarden/integrations/main/cli/estwarden -o ~/.local/bin/estwarden
chmod +x ~/.local/bin/estwarden
```

## Usage

```bash
estwarden threat       # 🟡 YELLOW — CTI: 21.9/100 (2026-03-20)
estwarden report       # Today's intelligence summary
estwarden narratives   # Active disinformation narratives (N1-N5)
estwarden campaigns    # Detected influence campaigns
estwarden history 14   # 14-day threat level trend
estwarden health       # API status
```

Requires: `curl`, `python3`, `jq` (optional).

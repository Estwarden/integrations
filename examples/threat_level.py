#!/usr/bin/env python3
"""Get current Baltic threat level."""
import json, urllib.request

with urllib.request.urlopen("https://estwarden.eu/api/threat-index") as r:
    d = json.loads(r.read())

emoji = {"GREEN": "🟢", "YELLOW": "🟡", "ORANGE": "🟠", "RED": "🔴"}.get(d["level"], "⚪")
print(f"{emoji} {d['level']} — CTI: {d['score']:.1f}/100 ({d['date']})")

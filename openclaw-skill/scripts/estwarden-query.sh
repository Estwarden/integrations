#!/bin/bash
# estwarden-query.sh — Query EstWarden public API
# No API key required. All data is public.
set -euo pipefail

API="https://estwarden.eu"

case "${1:-threat}" in
  threat|t)
    curl -s "$API/api/threat-index" | python3 -c "
import sys,json; d=json.load(sys.stdin)
e={'GREEN':'🟢','YELLOW':'🟡','ORANGE':'🟠','RED':'🔴'}.get(d.get('level',''),'⚪')
print(f\"{e} Baltic Threat Level: {d.get('level','?')}\")
print(f\"CTI Score: {d.get('score',0):.1f}/100\")
print(f\"Date: {d.get('date','?')}\")"
    ;;
  report|r)
    date="${2:-$(date +%Y-%m-%d)}"
    curl -s "$API/api/report/$date" | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(f\"Date: {d.get('date','?')} | Level: {d.get('threat_level',d.get('level','?'))}\")
print(f\"\n{d.get('summary','No report available')}\")
for i in d.get('indicators',[]):
    print(f\"  [{i['status']}] {i['category']}/{i['label']}: {i['finding']}\")"
    ;;
  narratives|narr|n)
    days="${2:-7}"
    curl -s "$API/api/influence/narratives?days=$days" | python3 -c "
import sys,json; d=json.load(sys.stdin)
items=d if isinstance(d,list) else d.get('narratives',[])
codes={'N1':'Russophobia/Persecution','N2':'War Escalation Panic','N3':'Aid=Theft','N4':'Delegitimization','N5':'Isolation/Victimhood'}
print(f'Active Narratives (last $days days):')
for i in items:
    c=i.get('code','?')
    print(f\"  {c} ({codes.get(c,'?')}): {i.get('count',0)} signals\")"
    ;;
  campaigns|camps|c)
    days="${2:-30}"
    curl -s "$API/api/influence/campaigns?days=$days" | python3 -c "
import sys,json; d=json.load(sys.stdin)
items=d if isinstance(d,list) else d.get('campaigns',[])
print(f'Influence Campaigns (last $days days):')
for c in items[:10]:
    print(f\"  [{c.get('severity','?')}] {c.get('name','?')}\")
    print(f\"    {c.get('summary','')[:150]}\")
if not items: print('  (none detected)')"
    ;;
  history|h)
    days="${2:-14}"
    curl -s "$API/api/history?days=$days" | python3 -c "
import sys,json; d=json.load(sys.stdin)
items=d if isinstance(d,list) else d.get('history',[])
for e in items:
    lvl=e.get('level','?')
    emoji={'GREEN':'🟢','YELLOW':'🟡','ORANGE':'🟠','RED':'🔴'}.get(lvl,'⚪')
    print(f\"  {e.get('date','?')} {emoji} {lvl:8s} {e.get('score',0):5.1f}/100\")"
    ;;
  health)
    curl -s "$API/health" | python3 -m json.tool
    ;;
  *)
    echo "Usage: estwarden-query.sh [threat|report|narratives|campaigns|history|health]"
    ;;
esac

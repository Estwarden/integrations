# EstWarden API Examples

Quick code snippets for every language.

## curl

```bash
# Threat level
curl -s https://estwarden.eu/api/threat-index | jq

# Today's report
curl -s https://estwarden.eu/api/today | jq .summary

# Narrative activity (last 7 days)
curl -s https://estwarden.eu/api/influence/narratives?days=7 | jq

# Threat history
curl -s https://estwarden.eu/api/history?days=30 | jq
```

## Python

```python
import urllib.request, json

def estwarden(path):
    with urllib.request.urlopen(f"https://estwarden.eu{path}") as r:
        return json.loads(r.read())

threat = estwarden("/api/threat-index")
print(f"{threat['level']} — {threat['score']:.1f}/100")

report = estwarden("/api/today")
print(report["summary"])
```

## Go

```go
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
)

func main() {
    resp, _ := http.Get("https://estwarden.eu/api/threat-index")
    defer resp.Body.Close()
    var data map[string]any
    json.NewDecoder(resp.Body).Decode(&data)
    fmt.Printf("%s — %.1f/100\n", data["level"], data["score"])
}
```

## JavaScript

```javascript
const resp = await fetch("https://estwarden.eu/api/threat-index");
const { level, score } = await resp.json();
console.log(`${level} — ${score.toFixed(1)}/100`);
```

## RSS Feed

```
https://estwarden.eu/feed.xml
```

Add to any RSS reader for daily intelligence updates.

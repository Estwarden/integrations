# EstWarden Grafana Dashboards

Pre-built Grafana dashboards for monitoring EstWarden data and pipeline health.

## Dashboards

### 1. Threat Overview (`threat-overview.json`)
- Composite Threat Index gauge (0-100 with color thresholds)
- Threat level history (30-day trend line)
- Active narrative breakdown (N1-N5 pie chart)
- Campaign count + latest campaign names
- Signal volume by source type (stacked bar)

### 2. Collector Health (`collector-health.json`)
- Per-source signal freshness (time since last signal)
- Signals ingested per hour (by source)
- Ingest API counters (signals, tags, errors)
- Container resource usage (CPU, memory)
- Failed DAG runs count

### 3. Influence Operations (`influence-ops.json`)
- Narrative classification over time (N1-N5 stacked area)
- Campaign timeline
- Top actors by signal volume
- Cross-platform correlation heatmap

## Setup

### Using EstWarden Public API as datasource

1. In Grafana, add a **JSON API** datasource:
   - URL: `https://estwarden.eu`
   - No auth required

2. Import the dashboard JSONs from this directory.

### Using Prometheus (self-hosted)

For self-hosted instances, metrics are available at internal endpoints.

## Example Queries

```promql
# Signals per source in last 24h
signals_24h

# Ingest rate
rate(ingest_signals_total[5m])

# Container memory
container_memory_usage_bytes{name=~"estwarden-.*"}
```

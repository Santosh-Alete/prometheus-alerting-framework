# Prometheus Alerting Framework

Production-ready alerting framework for Prometheus + Alertmanager + Grafana. Standardized alerting rules, routing configurations, and Grafana dashboards as code for multi-cluster Kubernetes environments.

## Overview

Managing alerting across multiple Kubernetes clusters and AWS accounts gets messy fast. This framework provides a structured, version-controlled approach to:

- **Alerting Rules** — SLO-based alerts for latency, error rates, and saturation
- **Recording Rules** — Pre-aggregated PromQL for dashboard performance
- **Alertmanager Config** — Routing, inhibition, and silencing with PagerDuty/Slack
- **Grafana Dashboards** — JSON dashboards provisioned as code

## Structure

```
├── alertmanager/
│   ├── alertmanager.yml          # Main routing config
│   └── templates/                # Notification templates
├── prometheus/
│   ├── rules/                    # Alerting rules by service
│   │   ├── slo-latency.yml
│   │   ├── slo-availability.yml
│   │   ├── infrastructure.yml
│   │   └── kubernetes.yml
│   └── recording/                # Recording rules
│       ├── slo-recording.yml
│       └── aggregations.yml
├── grafana/
│   └── dashboards/               # Dashboard JSON
│       ├── slo-overview.json
│       ├── cluster-health.json
│       └── service-latency.json
├── scripts/
│   ├── validate_rules.sh         # CI validation
│   └── deploy_dashboards.py      # Grafana API deployment
└── docs/
    └── runbook.md
```

## Alerting Philosophy

- **SLO-driven**: Alerts fire based on error budget burn rate, not arbitrary thresholds
- **Low noise**: Multi-window burn rate alerts reduce false positives
- **Actionable**: Every alert links to a runbook with remediation steps
- **Tiered severity**: critical → PagerDuty, warning → Slack, info → dashboard only

## Quick Start

```bash
# Validate all rules
./scripts/validate_rules.sh

# Deploy dashboards to Grafana
python scripts/deploy_dashboards.py --grafana-url http://grafana:3000 --api-key $GRAFANA_API_KEY

# Test alertmanager routing
amtool check-config alertmanager/alertmanager.yml
```

## SLO Alert Examples

### Latency SLO (99th percentile < 500ms)
```yaml
- alert: HighLatencyBurnRate
  expr: |
    (
      sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m])) by (service)
      /
      sum(rate(http_request_duration_seconds_count[5m])) by (service)
    ) < 0.99
  for: 5m
  labels:
    severity: warning
    slo: latency
```

### Availability SLO (99.9% success rate)
```yaml
- alert: HighErrorBurnRate
  expr: |
    1 - (
      sum(rate(http_requests_total{code!~"5.."}[5m])) by (service)
      /
      sum(rate(http_requests_total[5m])) by (service)
    ) > 0.001
  for: 5m
  labels:
    severity: critical
    slo: availability
```

## Requirements

- Prometheus 2.40+
- Alertmanager 0.25+
- Grafana 9.0+
- Python 3.9+ (for dashboard deployment)

## License

MIT

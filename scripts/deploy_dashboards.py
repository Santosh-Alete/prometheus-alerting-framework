#!/usr/bin/env python3
"""Deploy Grafana dashboards via API."""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError


def deploy_dashboard(grafana_url: str, api_key: str, dashboard_file: Path) -> bool:
    with open(dashboard_file) as f:
        payload = json.load(f)

    body = json.dumps({
        "dashboard": payload.get("dashboard", payload),
        "overwrite": True,
        "message": f"Deployed from CI: {dashboard_file.name}"
    }).encode()

    req = Request(
        f"{grafana_url.rstrip('/')}/api/dashboards/db",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        resp = urlopen(req)
        result = json.loads(resp.read())
        print(f"  ✅ {dashboard_file.name} -> {result.get('url', 'deployed')}")
        return True
    except HTTPError as e:
        print(f"  ❌ {dashboard_file.name} -> {e.code}: {e.read().decode()}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Deploy Grafana dashboards")
    parser.add_argument("--grafana-url", required=True)
    parser.add_argument("--api-key", default=os.environ.get("GRAFANA_API_KEY"))
    parser.add_argument("--dashboard-dir", default="grafana/dashboards")
    args = parser.parse_args()

    if not args.api_key:
        print("Error: --api-key or GRAFANA_API_KEY env var required")
        sys.exit(1)

    dashboard_dir = Path(args.dashboard_dir)
    files = sorted(dashboard_dir.glob("*.json"))

    if not files:
        print(f"No dashboards found in {dashboard_dir}")
        sys.exit(1)

    print(f"Deploying {len(files)} dashboards to {args.grafana_url}")
    failures = 0
    for f in files:
        if not deploy_dashboard(args.grafana_url, args.api_key, f):
            failures += 1

    if failures:
        print(f"\n{failures} deployment(s) failed")
        sys.exit(1)
    print("\nAll dashboards deployed successfully")


if __name__ == "__main__":
    main()

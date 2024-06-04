#!/bin/bash
set -euo pipefail

echo "Validating Prometheus rules..."

ERRORS=0

for f in prometheus/rules/*.yml prometheus/recording/*.yml; do
    echo -n "  Checking $f... "
    if promtool check rules "$f" 2>/dev/null; then
        echo "OK"
    else
        echo "FAILED"
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""
echo "Validating Alertmanager config..."
echo -n "  Checking alertmanager/alertmanager.yml... "
if amtool check-config alertmanager/alertmanager.yml 2>/dev/null; then
    echo "OK"
else
    echo "FAILED"
    ERRORS=$((ERRORS + 1))
fi

if [ $ERRORS -gt 0 ]; then
    echo ""
    echo "❌ $ERRORS validation errors found"
    exit 1
fi

echo ""
echo "✅ All rules and configs valid"

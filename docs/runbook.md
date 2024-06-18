# Alerting Runbook

## LatencySLOBurnRateCritical

**Severity:** Critical  
**SLO:** 99% of requests < 500ms

### Investigation
1. Check Grafana SLO dashboard for affected service
2. Look at p99 latency trend — is it a spike or gradual increase?
3. Check for recent deployments: `kubectl rollout history deployment/<service>`
4. Check downstream dependencies for latency

### Remediation
- If caused by deployment: `kubectl rollout undo deployment/<service>`
- If downstream: check dependency health dashboards
- If capacity: scale horizontally `kubectl scale deployment/<service> --replicas=<n>`

## AvailabilitySLOBurnRateCritical

**Severity:** Critical  
**SLO:** 99.9% success rate

### Investigation
1. Check error rate dashboard — which endpoints are failing?
2. Check application logs in Elasticsearch: `service:<name> AND level:error`
3. Check pod health: `kubectl get pods -n <namespace> | grep -v Running`
4. Check recent config changes or deployments

### Remediation
- Rollback if deployment-related
- Check database connectivity if 500s are DB-related
- Scale up if errors are from resource exhaustion

## NodeHighCPU / NodeHighMemory

**Severity:** Warning

### Investigation
1. Identify top consumers: check container CPU/memory in Grafana
2. Look for runaway processes or memory leaks
3. Check if HPA is scaling appropriately

### Remediation
- If single pod: restart or investigate the workload
- If cluster-wide: add nodes via cluster autoscaler or manual scaling
- Long-term: rightsize resource requests/limits

## DiskSpaceCritical

**Severity:** Critical

### Investigation
1. SSH to node or exec into pod
2. `df -h` to identify full filesystem
3. Check for large log files, temp files, or container images

### Remediation
- Clean up unused container images: `docker system prune`
- Rotate/compress logs
- Expand PV if using dynamic provisioning
- Add node if root disk is full

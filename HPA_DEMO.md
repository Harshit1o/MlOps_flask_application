# HPA Demo Guide

## Prerequisites
```bash
# Deploy the app
kubectl apply -f k8s/

# Port forward
kubectl port-forward svc/ml-flask-app 5000:80
```

## Demo Steps

### 1. Open Multiple Terminals

**Terminal 1 - Watch HPA:**
```bash
kubectl get hpa -w
```

**Terminal 2 - Watch Pods:**
```bash
kubectl get pods -w
```

**Terminal 3 - Generate Load:**
```bash
python load_test.py
```

### 2. What You'll See

**Before Load:**
```
NAME                REFERENCE                  TARGETS   MINPODS   MAXPODS   REPLICAS
ml-flask-app-hpa    Deployment/ml-flask-app    5%/70%    2         10        2
```

**During Load (CPU rises above 70%):**
```
ml-flask-app-hpa    Deployment/ml-flask-app    85%/70%   2         10        2
ml-flask-app-hpa    Deployment/ml-flask-app    85%/70%   2         10        4  <- Scaled up!
ml-flask-app-hpa    Deployment/ml-flask-app    78%/70%   2         10        4
ml-flask-app-hpa    Deployment/ml-flask-app    82%/70%   2         10        6  <- More scaling
```

**After Load (cooldown):**
```
ml-flask-app-hpa    Deployment/ml-flask-app    20%/70%   2         10        6
ml-flask-app-hpa    Deployment/ml-flask-app    15%/70%   2         10        4  <- Scaled down
ml-flask-app-hpa    Deployment/ml-flask-app    10%/70%   2         10        2  <- Back to min
```

### 3. Verify Scaling

```bash
# Check number of pods
kubectl get pods

# Check HPA events
kubectl describe hpa ml-flask-app-hpa

# Check pod resource usage
kubectl top pods
```

## Alternative Load Test Tools

### Using curl (simple loop)
```bash
for i in {1..1000}; do curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"features": [5.1, 3.5, 1.4, 0.2]}' & done
```

### Using Apache Bench
```bash
ab -n 10000 -c 100 http://localhost:5000/
```

### Using hey
```bash
hey -z 120s -c 50 http://localhost:5000/
```

## Tips for Demo

1. **Start with baseline**: Show 2 pods running normally
2. **Explain threshold**: CPU target is 70%
3. **Start load test**: Show CPU climbing
4. **Watch scaling**: Point out new pods being created
5. **Stop load**: Show pods scaling back down after cooldown
6. **Show metrics**: Use `kubectl top pods` to show actual CPU usage

## Troubleshooting

### HPA shows "unknown" for CPU
```bash
# Install metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### Not scaling up
- Increase load intensity in load_test.py
- Lower CPU threshold in k8s/hpa.yaml (e.g., 50% instead of 70%)
- Check if metrics-server is running: `kubectl get pods -n kube-system | grep metrics`

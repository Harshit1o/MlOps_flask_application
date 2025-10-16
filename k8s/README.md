# Kubernetes Deployment

## Deploy
```bash
kubectl apply -f k8s/
```

## Access Locally
```bash
kubectl port-forward svc/ml-flask-app 5000:80
```

Open http://localhost:5000

## Check Status
```bash
kubectl get pods
kubectl get hpa
```

## Delete
```bash
kubectl delete -f k8s/
```

## Resources
- CPU: 250m request, 1000m limit
- Memory: 512Mi request, 1Gi limit
- Autoscaling: 2-10 replicas at 70% CPU

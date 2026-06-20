# Kubernetes Deployment

## Gereksinimler

- Kubernetes 1.28+
- kubectl
- Helm 3.0+

## Kurulum

```bash
# Namespace oluştur
kubectl create namespace gitarchaeology

# ConfigMap oluştur
kubectl apply -f k8s/configmap.yaml

# Secret oluştur
kubectl apply -f k8s/secret.yaml

# Deployment'ları uygula
kubectl apply -f k8s/

# Durumu kontrol et
kubectl get pods -n gitarchaeology
```

## Servisler

| Servis | Replicas | Port |
|--------|----------|------|
| backend | 2 | 8000 |
| frontend | 2 | 80 |
| worker | 2 | - |

## Scaling

```bash
# Manual scaling
kubectl scale deployment backend --replicas=3 -n gitarchaeology

# Auto scaling
kubectl apply -f k8s/hpa.yaml
```

## Monitoring

```bash
# Pod logları
kubectl logs -f deployment/backend -n gitarchaeology

# Resource kullanımı
kubectl top pods -n gitarchaeology
```

## Rolling Update

```bash
# Image güncelle
kubectl set image deployment/backend backend=gitarchaeology/backend:latest -n gitarchaeology

# Durumu izle
kubectl rollout status deployment/backend -n gitarchaeology

# Geri al
kubectl rollout undo deployment/backend -n gitarchaeology
```

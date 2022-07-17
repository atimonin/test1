# test1
# a test app
For deploy to minikube:
- install and/or start minikube
- deploy postgresql:
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install test-postgers bitnami/postgresql \
  --set auth.username=blk_user \
  --set auth.database=blacklist \
  --set primary.persistence.enabled=false --set readReplicas.persistence.enabled=false
```
- build image (in minikube docker):
```
eval $(minikube docker-env)
docker build -t test1.0 .
```
- deplot test1 app
```
helm upgrade --install test1 kubernetes/test1
```

# test1
# a test app
For deploy to minikube:
- install and/or start minikube
- deploy postgresql:
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install test-postgres bitnami/postgresql \
  --set architecture=replication \
  --set auth.username=blk_user \
  --set auth.database=blacklist \
  --set primary.persistence.enabled=false --set readReplicas.persistence.enabled=false
```
- create table:
```
# make local access to postgres
export POSTGRES_PASSWORD=$(kubectl get secret --namespace default test-postgres-postgresql -o jsonpath="{.data.password}" | base64 -d)
kubectl port-forward --namespace default svc/test-postgres-postgresql 5432:5432 &
# create table
PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U blk_user -d blacklist -p 5432 <<__EOF
create table blacklist (
  seq_num serial PRIMARY KEY,
  ip_addr VARCHAR(64),
  path    VARCHAR(256),
  time    TIMESTAMP
);
__EOF
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

# SEZG583 – Student Course Registration Microservices

Two independently deployable FastAPI services:
1. Course Catalog Service
2. Enrollment Management Service

Each service owns its own SQLite database. Enrollment calls Course Catalog over synchronous REST to validate that a course exists.

## Prerequisites
- macOS, Python 3.11+ (project tested with Python 3.12)
- Docker Desktop
- kubectl
- Minikube
- Git

## A. Run locally (optional first check)
Terminal 1:
```bash
cd course-catalog-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p data
uvicorn app.main:app --reload --port 8001
```
Terminal 2:
```bash
cd enrollment-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p data
COURSE_CATALOG_URL=http://localhost:8001 uvicorn app.main:app --reload --port 8002
```
Swagger UI: http://localhost:8001/docs and http://localhost:8002/docs.

## B. Docker Compose deployment (recommended container integration test)
From the project root:
```bash
docker compose up --build -d
docker compose ps
```
Test:
```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
curl -X POST http://localhost:8001/courses \
  -H 'Content-Type: application/json' \
  -d '{"course_code":"CS501","title":"Cloud Computing","description":"Cloud fundamentals"}'
curl -X POST http://localhost:8002/enrollments \
  -H 'Content-Type: application/json' \
  -d '{"student_id":"STU1001","student_name":"Ravi Kumar","course_id":1}'
curl http://localhost:8002/enrollments
```
Stop:
```bash
docker compose down
```
Data remains in named volumes. To remove containers AND data:
```bash
docker compose down -v
```

## C. Minikube deployment
Start Docker Desktop first, then from project root:
```bash
minikube start --driver=docker
minikube status
kubectl get nodes
```
Build images directly into Minikube's image store:
```bash
minikube image build -t course-catalog:1.0 ./course-catalog-service
minikube image build -t enrollment-service:1.0 ./enrollment-service
```
Apply namespace, storage, then services:
```bash
kubectl apply -f kubernetes/00-namespace.yaml
kubectl apply -f kubernetes/01-storage.yaml
kubectl apply -f kubernetes/02-course-catalog.yaml
kubectl apply -f kubernetes/03-enrollment.yaml
```
Wait and inspect:
```bash
kubectl get pvc -n student-registration
kubectl get pods -n student-registration -w
kubectl get deployments,services -n student-registration
kubectl describe deployment course-catalog -n student-registration
kubectl logs deployment/course-catalog -n student-registration
kubectl logs deployment/enrollment -n student-registration
```
Open local tunnels in two separate terminals:
```bash
kubectl port-forward -n student-registration service/course-catalog 8001:8000
```
```bash
kubectl port-forward -n student-registration service/enrollment 8002:8000
```
Then use Postman or curl against localhost:8001 and localhost:8002. Inside the cluster, Enrollment uses `http://course-catalog:8000`, resolved by Kubernetes DNS.

## D. API test sequence
1. GET `http://localhost:8001/health`
2. POST `http://localhost:8001/courses` with:
```json
{"course_code":"CS501","title":"Cloud Computing","description":"Cloud fundamentals"}
```
Expected: 201 Created and course `id` (normally 1 on a fresh database).
3. GET `http://localhost:8001/courses`
4. POST `http://localhost:8002/enrollments` with:
```json
{"student_id":"STU1001","student_name":"Ravi Kumar","course_id":1}
```
Expected: 201 Created and `status` ACTIVE.
5. GET `http://localhost:8002/enrollments`
6. GET `http://localhost:8002/students/STU1001/enrollments`
7. DELETE `http://localhost:8002/enrollments/1`
Expected: response status CANCELLED.
8. Try to enroll again after cancellation; it is permitted by this simple model. Try a duplicate while ACTIVE; expected 409.
9. Try course_id 999; expected 404.

## E. Kubernetes dashboard
```bash
minikube dashboard
```
Capture screenshots of:
- Namespace student-registration
- Deployments course-catalog and enrollment
- Pods in Running/Ready state
- Services and PVCs

## F. Useful troubleshooting
- `ImagePullBackOff`: ensure image was built using `minikube image build` and image name matches YAML.
- Pod pending: inspect `kubectl describe pod <pod> -n student-registration`; check PVC status.
- Enrollment returns 503: check catalog pod/service and logs; confirm `COURSE_CATALOG_URL=http://course-catalog:8000`.
- Port-forward fails: check service names with `kubectl get svc -n student-registration`.
- Reset all app resources:
```bash
kubectl delete namespace student-registration
```
Then reapply manifests. This deletes PVCs and their data.

## G. Clean up
```bash
kubectl delete namespace student-registration
minikube stop
```
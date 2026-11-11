# SEZG583 – Scalable Services Assignment
## Student Course Registration System

**Student name:** ****
**Student ID:** ****  
**Course:** SEZG583 – Scalable Services  
**Submission date:** 12 November 2026

## 1. Abstract
This project implements a student course registration application using two independently deployable microservices: Course Catalog and Enrollment Management. Both services expose REST APIs using FastAPI and maintain separate SQLite databases. The services are packaged as Docker containers and deployed to a local Kubernetes cluster using Minikube.

## 2. Objectives
- Design a microservices-based application.
- Identify business capabilities, commands and queries.
- Implement two independent services.
- Demonstrate REST-based service collaboration.
- Containerize each service independently.
- Deploy and inspect the application on Kubernetes/Minikube.

## 3. Functional requirements
- Create, list, retrieve, update and delete courses.
- Register a student for an existing course.
- Prevent duplicate active enrollment for the same student/course.
- Retrieve enrollments by enrollment ID and student ID.
- Cancel an enrollment.

## 4. Architecture and service decomposition
Insert architecture diagram. Course Catalog owns course data. Enrollment owns enrollment data. Enrollment calls Course Catalog synchronously to validate course existence before saving a registration.

## 5. Commands and queries
Commands: create/update/delete course, create/cancel enrollment.  
Queries: list/get courses, list/get enrollments, list student enrollments.  
Include API endpoint tables from the project README.

## 6. Technology selection
Python, FastAPI, SQLAlchemy, SQLite, REST/HTTP, Docker, Kubernetes, Minikube, Postman and GitHub. Explain SQLite selection as a low-dependency local-lab choice and document its single-replica limitation.

## 7. Implementation
Describe each service, its endpoints, validation, error handling, database ownership and inter-service call. Add source-code structure and repository URLs.

## 8. Containerization
Describe the separate Dockerfiles and images. Include `docker compose ps` and API test evidence.

## 9. Kubernetes deployment
Describe namespace, Deployments, ClusterIP Services, PVCs, probes, resource requests/limits and service DNS. Include `kubectl get pods`, `kubectl get svc`, `kubectl get pvc` output.

## 10. Testing and results
Add Postman screenshots for:
- Create course (201)
- List courses (200)
- Successful enrollment (201)
- Unknown course (404)
- Duplicate active enrollment (409)
- Cancel enrollment (200)
- Health checks (200)

## 11. Dashboard evidence
Add Minikube Dashboard screenshots showing both Deployments, Pods, Services and PVCs.

## 12. Limitations and future enhancements
Discuss SQLite single-replica limitation, lack of authentication, no waitlist/capacity management, and possible future adoption of managed relational databases, API security, metrics, tracing and CI/CD.

## 13. Conclusion
Summarize how the project demonstrates service decomposition, independent implementation, REST collaboration, containerization and Kubernetes deployment.


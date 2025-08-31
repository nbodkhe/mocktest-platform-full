# High-Level Design (HLD) - Mocktest Platform

## 🎯 Goal
Build a scalable **mock test platform** with:
- User authentication
- Test creation and question management
- Test sessions and submissions
- Result computation and leaderboard analytics
- Observability & monitoring

---

## 🏗️ System Components
- **FastAPI Application**  
  - Routers: `auth`, `tests`, `questions`, `sessions`, `submissions`, `results`, `leaderboard`, `predict`, `health`.
  - Middleware: Request logging, request-id, GZip.
  - Observability: Prometheus metrics endpoint, structured logs.

- **PostgreSQL**  
  - Primary relational database
  - Alembic for migrations

- **Redis**  
  - Celery task broker + result backend
  - Caching support

- **Celery Workers**  
  - Asynchronous jobs for heavy computations:
    - Recalculate score snapshots
    - Leaderboard updates
    - Score distribution histogram

- **Nginx**  
  - Reverse proxy
  - Serves API and `/docs`
  - Security headers & TLS termination (in prod)

- **Monitoring & Health**
  - `/readyz`, `/api/v1/healthz` for probes
  - `/metrics` for Prometheus

---

## 📊 Key Flows
1. **Auth** → Signup/Login → JWT token
2. **Test Authoring** → Create test → Add questions → Publish
3. **Exam Session** → User starts → Submits answers
4. **Scoring** → Worker computes snapshot + leaderboard
5. **Analytics** → Results, leaderboard, score distributions

---

## ⚙️ Non-Functional Requirements
- **Scalable**: stateless API, distributed workers
- **Secure**: JWT, bcrypt passwords
- **Reliable**: idempotent submissions, migrations
- **Observable**: logs + metrics

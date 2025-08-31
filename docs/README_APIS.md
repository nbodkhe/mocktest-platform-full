# API Documentation - Mocktest Platform

Base URL: `http://localhost:8080`

---

## 🔐 Auth APIs
- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

## 🧪 Test APIs
- `POST /api/v1/tests` → create test
- `GET /api/v1/tests` → list tests
- `GET /api/v1/tests/{id}`
- `PATCH /api/v1/tests/{id}`
- `DELETE /api/v1/tests/{id}`

## ❓ Question APIs
- `POST /api/v1/questions`
- `GET /api/v1/tests/{id}/questions`

## 📘 Session APIs
- `POST /api/v1/sessions`
- `GET /api/v1/sessions?test_id=`
- `PATCH /api/v1/sessions/{id}`

## 📝 Submission APIs
- `POST /api/v1/submissions`
- `GET /api/v1/submissions?test_id=`

## 📊 Results & Analytics
- `GET /api/v1/results/{test_id}/me`
- `GET /api/v1/leaderboard/{test_id}`
- `GET /api/v1/results/{test_id}/distribution`

## 🤖 Predict (optional)
- `POST /api/v1/predict`

## 💚 Health
- `GET /api/v1/healthz`
- `GET /readyz`
- `GET /metrics`

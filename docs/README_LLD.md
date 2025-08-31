# Low-Level Design (LLD) - Mocktest Platform

## 🗄️ Database Schema

- **users**
  - `id`, `email`, `name`, `password_hash`, `is_admin`, `created_at`
- **tests**
  - `id`, `name`, `duration_minutes`, `mark_correct`, `mark_incorrect`, `subjects (jsonb)`, `status`, `created_at`
- **questions**
  - `id`, `test_id FK`, `subject`, `stem`, `options (jsonb)`, `correct_index`, `difficulty`
- **test_sessions**
  - `id`, `test_id FK`, `user_id FK`, `start_at`, `end_at`, `status`, `ip`, `fingerprint`
- **submissions**
  - `id`, `test_id FK`, `user_id FK`, `question_id FK`, `chosen_index`, `is_correct`, `answered_at`
- **score_snapshots**
  - `id`, `test_id FK`, `user_id FK`, `total_score`, `subject_scores (jsonb)`, `attempted`, `correct`, `incorrect`
- **leaderboard**
  - `id`, `test_id FK`, `user_id FK`, `rank`, `percentile`, `total_score`
- **score_distributions**
  - `id`, `test_id FK`, `subject`, `histogram (jsonb)`, `n`, `min`, `max`

---

## 📡 API Endpoints (Summary)

- **Auth**: `/signup`, `/login`, `/me`
- **Tests**: CRUD
- **Questions**: CRUD
- **Sessions**: start, get, end
- **Submissions**: submit, list
- **Results**: `/me`, leaderboard, distributions
- **Predict**: optional ML scoring
- **Health**: `/healthz`, `/readyz`, `/metrics`

---

## 🔄 Sequence Flow (Example: Submitting Answer)

1. `POST /submissions`
2. Validate session active
3. Check correctness → mark `is_correct`
4. Save submission (unique key ensures idempotency)
5. Fire **Celery job**:
   - Update `score_snapshots`
   - Update `leaderboard`
   - Update `score_distributions`
6. API responds with `{ is_correct, answered_at }`

---

## 🧩 Security
- JWT token in `Authorization: Bearer`
- Passwords stored with `bcrypt`
- Admin role required for authoring APIs

# Algorithms & Logic - Mocktest Platform

## 1. Authentication
- Passwords → `bcrypt` hash
- JWT token issuance with expiry
- `is_admin` flag checked for authoring routes

## 2. Test Scoring
- Correctness decided by comparing `chosen_index` with `correct_index`

## 3. Snapshot Update (Celery Task)
- Aggregate per user per test:
  - attempted = count(submissions)
  - correct = count(is_correct=True)
  - incorrect = count(is_correct=False)
  - total_score = formula above
  - subject_scores = JSON aggregated by subject

## 4. Leaderboard Ranking
- Order by `total_score DESC`
- Ties broken by `tiebreaker JSON` (e.g., fastest end time)
- Percentile = `(N - rank) / N * 100`

## 5. Score Distribution
- Group `total_score` into histogram bins
- Track min, max, average
- Store per subject if required

## 6. Predict API (optional ML)
- Input: `{ attempted, correct, incorrect, subject_scores }`
- Logic:
  - Rule-based baseline: linear regression-like formula
  - Future: ML model integration via Celery task

## 7. Health & Metrics
- `/healthz` → DB + Redis ping
- `/readyz` → liveness probe
- `/metrics` → Prometheus scrape

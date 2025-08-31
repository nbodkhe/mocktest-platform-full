from app.infra.broker import celery_app

@celery_app.task
def finalize_test_job(test_id: int):
    # Placeholder; Pack C will implement finalize → histograms → leaderboard materialization
    return {"test_id": test_id, "status": "queued"}

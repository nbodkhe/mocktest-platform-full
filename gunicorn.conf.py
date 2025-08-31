import multiprocessing, os
bind = "0.0.0.0:%s" % os.getenv("PORT", "8000")
workers = int(os.getenv("WORKERS", str(multiprocessing.cpu_count() * 2 + 1)))
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
graceful_timeout = 30
keepalive = 5

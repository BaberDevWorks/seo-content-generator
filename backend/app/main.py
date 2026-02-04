from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.models.job import GenerationJob, JobStatus
from app.models.requests import GenerateArticleRequest
from app.services.job_store import get_all_jobs, save_job, get_job
from app.services.job_store import (
    save_job,
    get_job,
    save_job_result,
    get_job_result,
)

from app.services.job_runner import run_full_generation

app = FastAPI(title="SEO Content Generator", version="1.0.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/jobs")
def create_job(request: GenerateArticleRequest):
    job = GenerationJob.create(
        topic=request.topic,
        language=request.language,
        target_word_count=request.target_word_count,
    )
    save_job(job)
    return job

@app.get("/jobs/{job_id}")
def fetch_job(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/jobs")
def fetch_all_jobs():
    return get_all_jobs()

@app.post("/jobs/{job_id}/run")
def run_job(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    try:
        result = run_full_generation(job)
        job.status = JobStatus.completed
        save_job(job)
        save_job_result(job_id, result)

        return {"status": "completed", "job_id": job_id}
    except Exception as e:
        job.status = JobStatus.failed
        job.error = str(e)
        save_job(job)
        save_job_result(job_id, {"status": "failed", "detail": str(e), "error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/jobs/{job_id}/result")
def fetch_job_result(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    result = get_job_result(job_id)
    if not result:
        if job.status == JobStatus.failed:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "failed",
                    "detail": job.error or "Generation failed",
                    "job_id": job_id,
                },
            )

        return JSONResponse(
            status_code=202,
            content={
                "status": job.status.value if hasattr(job.status, "value") else str(job.status),
                "detail": job.current_step or "Processing...",
                "job_id": job_id,
            },
        )

    return result
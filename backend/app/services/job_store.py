from typing import Dict
from app.models.job import GenerationJob


JOB_STORE: Dict[str, GenerationJob] = {}
JOB_RESULTS: Dict[str, dict] = {}

def save_job(job: GenerationJob):
    JOB_STORE[job.id] = job


def get_job(job_id: str) -> GenerationJob | None:
    return JOB_STORE.get(job_id)

def get_all_jobs() -> list[GenerationJob]:
    return list(JOB_STORE.values())

def save_job_result(job_id: str, result: dict):
    JOB_RESULTS[job_id] = result

def get_job_result(job_id: str) -> dict | None:
    return JOB_RESULTS.get(job_id)
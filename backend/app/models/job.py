from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional
import uuid


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class GenerationJob(BaseModel):
    id: str
    topic: str
    language: str = "en"
    target_word_count: int = 1500
    status: JobStatus
    current_step: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(topic: str, language: str, target_word_count: int):
        now = datetime.utcnow()
        return GenerationJob(
            id=str(uuid.uuid4()),
            topic=topic,
            language=language,
            target_word_count=target_word_count,
            status=JobStatus.pending,
            created_at=now,
            updated_at=now,
        )

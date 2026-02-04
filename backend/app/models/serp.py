from pydantic import BaseModel

class SerpResult(BaseModel):
    rank: int
    url: str
    title: str
    snippet: str

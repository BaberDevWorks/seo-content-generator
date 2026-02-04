from pydantic import BaseModel

class GenerateArticleRequest(BaseModel):
    topic: str
    language: str = "en"
    target_word_count: int = 1500

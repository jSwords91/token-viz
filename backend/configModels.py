from pydantic import BaseModel
from typing import List

class Config(BaseModel):
    """Configuration for the FastAPI app metadata."""
    TITLE: str = "Tokenizer API"
    DESCRIPTION: str = "An API for vizualising tokenization text using various models"
    VERSION: str = "1.0.0"

class AvailableTokenizers(BaseModel):
    """Available tokenizers for the application."""
    AVAILABLE_TOKENIZERS: List[str] = [
        "gpt2",
        "bert-base-uncased",
        "roberta-base",
        "t5-small",
        "xlnet-base-cased"
    ]

class Settings(BaseModel):
    """Settings for the application."""
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]

    # Application settings
    FRONTEND_DIR: str = "frontend"
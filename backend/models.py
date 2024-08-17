from typing import List, Dict
from pydantic import BaseModel, Field


class TokenizeRequest(BaseModel):
    text: str = Field(..., description="The text to tokenize")
    tokenizer: str = Field(..., description="The tokenizer to use")

class TokenizeResponse(BaseModel):
    tokens: List[str]
    count: int = Field(..., description="The number of tokens used")
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer

from .tokenizerManager import TokenizerManager
from .models import TokenizeRequest, TokenizeResponse
from .configModels import Config, Settings, AvailableTokenizers

def create_app() -> FastAPI:

    config = Config()
    settings = Settings()
    available_tokenizers = AvailableTokenizers()

    app = FastAPI(
        title=config.TITLE,
        description=config.DESCRIPTION,
        version=config.VERSION,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    tokenizer_manager = TokenizerManager(available_tokenizers)

    @app.post("/api/tokenize", response_model=TokenizeResponse)
    async def tokenize(request: TokenizeRequest) -> TokenizeResponse:
        try:
            tokenizer = tokenizer_manager.get_tokenizer(request.tokenizer)
            tokens = tokenizer.tokenize(request.text)
            return TokenizeResponse(tokens=tokens, count=len(tokens))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    app.mount("/", StaticFiles(directory=settings.FRONTEND_DIR, html=True), name="frontend")

    return app
